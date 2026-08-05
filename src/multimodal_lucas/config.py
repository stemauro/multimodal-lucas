# SPDX-FileCopyrightText: 2026 Stefano Maurogiovanni <s.maurogiovanni@gmx.de>
#
# SPDX-License-Identifier: MIT

from enum import StrEnum
from functools import partial

GISCO_PHOTOS_BASE_URL = "https://gisco-services.ec.europa.eu/lucas/photos"

LUCAS_YEARS = ["2006", "2009", "2012", "2015", "2018", "2022"]


class LucasDirection(StrEnum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    POINT = "point"
    CLOSEUP = "crop"

    def _fmt_suffix_legacy(self):
        return self.value[0].upper()

    def _fmt_suffix_latest(self):
        return self.value.capitalize()

    def to_suffix(self, year: str):
        if int(year) < 2022:
            return self._fmt_suffix_legacy()
        return self._fmt_suffix_latest()


def get_legacy_filename_pattern(year: str, *, direction: LucasDirection) -> str:
    return f"{{}}{direction.to_suffix(year)}"


def get_latest_filename_pattern(year: str, *, direction: LucasDirection) -> str:
    suffix = direction.to_suffix(year) + (
        "LC1" if direction == LucasDirection.CLOSEUP else ""
    )
    return f"{year}{{}}LCLU_{suffix}"


FILENAME_PATTERNS = {
    "2006": partial(get_legacy_filename_pattern, year="2006"),
    "2009": partial(get_legacy_filename_pattern, year="2009"),
    "2012": partial(get_legacy_filename_pattern, year="2012"),
    "2015": partial(get_legacy_filename_pattern, year="2015"),
    "2018": partial(get_legacy_filename_pattern, year="2018"),
    "2022": partial(get_latest_filename_pattern, year="2022"),
}


def get_url_pattern(year: str, direction: LucasDirection, fmt: str = "jpg") -> str:
    return f"{GISCO_PHOTOS_BASE_URL}/{{}}/{{}}/{{}}/{FILENAME_PATTERNS[year](direction=direction)}.{fmt}"
