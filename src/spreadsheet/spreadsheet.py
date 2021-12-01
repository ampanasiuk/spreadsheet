from typing import Union


class Coord:
    def __init__(self, s: str):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError


CoordLike = Union[Coord, str]


class SpreadsheetError(Exception):
    pass


class Spreadsheet:
    pass
