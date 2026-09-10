# SPDX-FileCopyrightText: 2026 Stefano Maurogiovanni <s.maurogiovanni@gmx.de>
#
# SPDX-License-Identifier: MIT

"""
Custom test fixtures.
"""

import datetime as dt

import pytest
from polars import DataFrame

from multimodal_lucas.config import TARGET_COLUMNS

DUMMY_VALUES = (
    12345,
    "IT",
    "IT1",
    "IT11",
    "IT111",
    12.1223,
    73.4356,
    "B99",
    dt.date(2005, 7, 14),
)


@pytest.fixture
def generic_dataframe() -> DataFrame:
    return DataFrame(dict(zip(TARGET_COLUMNS["2018"], DUMMY_VALUES, strict=True)))


@pytest.fixture
def canonical_dataframe() -> DataFrame:
    return DataFrame(dict(zip(TARGET_COLUMNS["2022"], DUMMY_VALUES, strict=True)))
