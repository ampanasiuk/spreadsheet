import re
from typing import Union

from spreadsheet import SpreadsheetError


COORD_PATTERN = re.compile(r'([A-Z]+)([1-9][0-9]*)')


class Coord:
    def __init__(self, s: str):
        if match := COORD_PATTERN.fullmatch(s):
            self.col = match.group(1)
            self.row = int(match.group(2))
        else:
            raise SpreadsheetError("invalid coords")

    @staticmethod
    def make(obj):
        if isinstance(obj, Coord):
            return obj
        return Coord(obj)

    def _key(self):
        return self.col, self.row

    def __eq__(self, other):
        if not isinstance(other, Coord):
            if not isinstance(other, str):
                return False
            other = Coord(other)
        return self._key() == other._key()

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return f"{self.col}{self.row}"


CoordLike = Union[Coord, str]
