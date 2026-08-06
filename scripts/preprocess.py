# SPDX-FileCopyrightText: 2026 Stefano Maurogiovanni <s.maurogiovanni@gmx.de>
#
# SPDX-License-Identifier: MIT

"""Load, filter, augment and clean LUCAS metadata into an Hugging Face dataset."""

import asyncio
from argparse import ArgumentParser
from asyncio import Queue
from collections.abc import MutableSequence, Sequence
from itertools import batched, zip_longest
from typing import Any, Protocol

import polars as pl
import requests
from aiohttp import ClientSession
from datasets import Dataset
from polars import selectors as cs
from tqdm.asyncio import tqdm

from multimodal_lucas import project_root
from multimodal_lucas.config import LUCAS_YEARS, LucasDirection, get_url_pattern
from multimodal_lucas.data import load_dataframe, save_dataframe


class ScriptArgs(Protocol):
    year: str
    num_tasks: int


def is_resource_found(url: str) -> bool:
    return requests.get(url).ok


def chunk_according_to_tasks(data: Sequence[Any], num_tasks: int) -> list[tuple[Any]]:
    num_samples = len(data)
    chunk_size = num_samples // num_tasks

    if num_samples % num_tasks == 0:
        return list(batched(data, n=chunk_size))

    sentinel = chunk_size * num_tasks

    fitting, overflowing = data[:sentinel], data[sentinel:]
    fitting_chunked = batched(fitting, n=chunk_size)

    balanced_chunks = [
        f if o is None else (*f, o)
        for f, o in zip_longest(fitting_chunked, overflowing)
    ]

    return balanced_chunks


def compile_url_expr(year: str, direction: LucasDirection) -> pl.Expr:
    """Compile a Polars format expression to generate the full photo URL"""

    url_pattern = get_url_pattern(year=year, direction=direction)
    url_alias = f"PHOTO_{direction.value.upper()}_URL"

    return pl.format(
        url_pattern,
        pl.col("POINT_NUTS0"),
        pl.col("POINT_ID").str.head(3),
        pl.col("POINT_ID").str.slice(3, 3),
        pl.col("POINT_ID"),
    ).alias(url_alias)


def lowercase_column_names(dataset: Dataset) -> Dataset:
    column_names = dataset.column_names
    name_mapping = dict(zip(column_names, map(str.lower, column_names), strict=True))

    return dataset.rename_columns(name_mapping)


async def fetch_status_codes(
    resources: Sequence[dict[str, str]],
    session: ClientSession,
    queue: Queue[dict[str, int | str]],
    progress_bar: tqdm,
) -> None:
    for resource in resources:
        result = {"POINT_ID": resource.pop("POINT_ID")}
        for name, url in resource.items():
            async with session.head(url) as headers:
                key = name.replace("URL", "HTTP_STATUS")
                result[key] = headers.status
        await queue.put(result)
        progress_bar.update(1)


async def flush_to_list(
    queue: Queue[dict[str, int | str]],
    results: MutableSequence[dict[str, int | str]],
    progress_bar: tqdm,
) -> MutableSequence[dict[str, int | str]]:
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        results.append(item)
        queue.task_done()
        progress_bar.update(1)
    return results


async def main(args: ScriptArgs) -> None:

    # 1. Load dataset and compile file URLs ###

    is_valid_crop = pl.col("SURVEY_LC1").str.starts_with("B") & ~pl.col(
        "SURVEY_LC1"
    ).str.contains("x")

    df_raw = load_dataframe(
        "csv",
        path=project_root / "data" / "raw" / f"EU_LUCAS_{args.year}.csv",
        infer_schema=False,
    )

    url_exprs = [compile_url_expr(args.year, direction) for direction in LucasDirection]
    df_augmented = (
        df_raw.select("POINT_ID", "POINT_NUTS0", "SURVEY_LC1")
        .filter(is_valid_crop)
        .with_columns(url_exprs)
    )

    # 2. Validate URLs by storing their response code upon fetch

    queue = Queue()
    results = []

    data = df_augmented.select("POINT_ID", cs.starts_with("PHOTO")).rows(named=True)
    data_chunks = chunk_according_to_tasks(data, num_tasks=args.num_tasks)

    fetch_progress = tqdm(total=len(data), desc="Fetching headers", unit="url")
    flush_progress = tqdm(total=len(data), desc="Flushing status codes", unit="item")

    async with ClientSession() as session:
        fetch_tasks = [
            asyncio.create_task(
                fetch_status_codes(chunk, session, queue, progress_bar=fetch_progress)
            )
            for chunk in data_chunks
        ]
        flush_task = asyncio.create_task(
            flush_to_list(queue, results, progress_bar=flush_progress)
        )

        await asyncio.gather(*fetch_tasks)
        await queue.put(None)

        await queue.join()
        await flush_task

    df_valiadated = df_augmented.join(pl.DataFrame(results), on="POINT_ID")

    # 3. Remove entries bereft of available photos

    df_clean = df_valiadated.filter(
        pl.any_horizontal(cs.ends_with("HTTP_STATUS").eq(200))
    )

    output_dir = project_root / "data" / "processed" / args.year
    output_dir.mkdir(exist_ok=True, parents=True)
    save_dataframe(df_clean, fmt="jsonl", path=output_dir / "manifest.jsonl")

    # 4. Convert dataframe to a HuggingFace dataset save it locally

    df_clean = load_dataframe(
        "jsonl", path=project_root / "data/processed/2022/manifest.jsonl"
    )

    dataset_clean = lowercase_column_names(
        Dataset.from_dict(df_clean.to_dict(as_series=False))
    )
    dataset_clean.save_to_disk(str(output_dir))


""

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Data preparation script.", prog="uv run scripts/preprocess.py"
    )

    parser.add_argument(
        "--year",
        type=str,
        choices=LUCAS_YEARS,
        default="2022",
        help="The LUCAS reference year (default: %(default)s)",
    )
    parser.add_argument(
        "--num_tasks",
        type=int,
        default=4,
        help="The number of asynchronous tasks performing URLs validation (default: %(default)s)",
    )

    args = parser.parse_args()

    asyncio.run(main(args))
