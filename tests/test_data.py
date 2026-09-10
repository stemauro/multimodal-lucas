# SPDX-FileCopyrightText: 2026 Stefano Maurogiovanni <s.maurogiovanni@gmx.de>
#
# SPDX-License-Identifier: MIT

"""
Tests for dataframe and dataset wrangling.
"""

import pytest
from polars import DataFrame
from polars.testing import assert_frame_equal

from multimodal_lucas.data import rename_canonical


@pytest.mark.usefixtures("generic_dataframe", "canonical_dataframe")
def test_rename_canonical(
    generic_dataframe: DataFrame, canonical_dataframe: DataFrame
) -> None:
    assert_frame_equal(
        rename_canonical(generic_dataframe, current_year="2018"), canonical_dataframe
    )
