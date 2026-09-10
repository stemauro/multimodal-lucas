# SPDX-FileCopyrightText: 2026 Stefano Maurogiovanni <s.maurogiovanni@gmx.de>
#
# SPDX-License-Identifier: MIT

"""
Tests for naming conventions and configuration helpers.
"""

import pytest

from multimodal_lucas.config import (
    LucasDirection,
    get_latest_filename_pattern,
    get_legacy_filename_pattern,
    get_url_pattern,
)


def test_direction_suffix_2018_format() -> None:
    point_direction = LucasDirection.POINT

    assert point_direction.to_suffix("2018") == "P"


def test_direction_suffix_2022_format() -> None:
    point_direction = LucasDirection.POINT

    assert point_direction.to_suffix("2022") == "Point"


def test_legacy_filename_pattern() -> None:

    assert get_legacy_filename_pattern("2018", direction=LucasDirection.NORTH) == "{}N"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({"year": "2022", "direction": LucasDirection.NORTH}, "2022{}LCLU_North"),
        (
            {"year": "2022", "direction": LucasDirection.CLOSEUP},
            "2022{}LCLU_CropLC1",
        ),
    ],
)
def test_latest_filename_pattern(
    test_input: dict[str, LucasDirection], expected: str
) -> None:
    assert get_latest_filename_pattern(**test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {"year": "2018", "direction": LucasDirection.WEST},
            "https://gisco-services.ec.europa.eu/lucas/photos/2018/{}/{}/{}/{}W.jpg",
        ),
        (
            {"year": "2022", "direction": LucasDirection.WEST},
            "https://gisco-services.ec.europa.eu/lucas/photos/2022/{}/{}/{}/2022{}LCLU_West.jpg",
        ),
        (
            {"year": "2022", "direction": LucasDirection.CLOSEUP},
            "https://gisco-services.ec.europa.eu/lucas/photos/2022/{}/{}/{}/2022{}LCLU_CropLC1.jpg",
        ),
        (
            {"year": "2022", "direction": LucasDirection.CLOSEUP, "fmt": "png"},
            "https://gisco-services.ec.europa.eu/lucas/photos/2022/{}/{}/{}/2022{}LCLU_CropLC1.png",
        ),
    ],
)
def test_get_url_pattern(test_input: dict[str, LucasDirection], expected: str) -> None:
    assert get_url_pattern(**test_input) == expected
