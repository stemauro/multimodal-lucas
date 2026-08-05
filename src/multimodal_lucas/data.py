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
    "tsv": partial(pl.read_csv, separator="\t"),
}


def load_dataframe(
    fmt: str | DataframeFormat,
    path: str | Path,
    strict=True,
    **polars_specific_loading_kwargs,
):
    """A convenient wrapper around a polars loader function, i.e., polars.load_csv(),
    agnostic with respect to the data format and with controlled unstrict loading option
    """

    fmt = DataframeFormat(fmt)
    path = Path(path)

    polars_specific_loading_kwargs["infer_schema"] = strict
    return POLARS_LOADERS[fmt](path, **polars_specific_loading_kwargs)
