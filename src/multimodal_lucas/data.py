# SPDX-FileCopyrightText: 2026 Stefano Maurogiovanni <s.maurogiovanni@gmx.de>
#
# SPDX-License-Identifier: MIT

"""Dataset and dataframes management utilities."""

from enum import StrEnum, auto
from functools import partial
from pathlib import Path

import polars as pl


class DataframeFormat(StrEnum):
    CSV = (auto(),)
    JSON = (auto(),)
    JSONL = (auto(),)
    PARQUET = (auto(),)
    TSV = (auto(),)


POLARS_LOADERS = {
    "csv": pl.read_csv,
    "json": pl.read_json,
    "jsonl": pl.read_ndjson,
    "parquet": pl.read_parquet,
    "tsv": partial(pl.read_csv, separator="\t"),
}

POLARS_WRITERS = {
    "csv": pl.DataFrame.write_csv,
    "json": pl.DataFrame.write_json,
    "jsonl": pl.DataFrame.write_ndjson,
    "parquet": pl.DataFrame.write_parquet,
    "tsv": partial(pl.DataFrame.write_csv, separator="\t"),
}


def load_dataframe(
    fmt: str | DataframeFormat, path: str | Path, **loader_specific_kwargs
):
    """A convenient wrapper around a polars loader function, i.e., polars.load_csv(),
    agnostic with respect to the data format and with controlled unstrict loading option
    """

    fmt = DataframeFormat(fmt)
    path = Path(path)

    return POLARS_LOADERS[fmt](path, **loader_specific_kwargs)


def save_dataframe(
    frame: pl.DataFrame,
    fmt: str | DataframeFormat,
    path: str | Path,
    **polars_writing_kwargs,
):
    """A convenient wrapper around a polars loader function, i.e., polars.load_csv(),
    agnostic with respect to the data format and with controlled unstrict loading option
    """

    fmt = DataframeFormat(fmt)
    path = Path(path)

    return POLARS_WRITERS[fmt](frame, path, **polars_writing_kwargs)
