from typing import Dict

from spreadsheet.cellstorage import CellStorage
from spreadsheet.coord import Coord
from spreadsheet.coord import CoordLike
from spreadsheet.formula import const
from spreadsheet.formula import formula
from spreadsheet.spreadsheet_error import SpreadsheetError


class Spreadsheet(CellStorage):
    def __init__(self):
        self.data: Dict[Coord, formula] = {}

    def __getitem__(self, item):
        if not isinstance(item, CoordLike):
            raise TypeError
        try:
            item = Coord.make(item)
        except SpreadsheetError as e:
            raise KeyError(e)
        if item in self.data:
            return self.data[item].value(self)
        return 0

    def __setitem__(self, item, value):
        if not isinstance(item, CoordLike):
            raise TypeError
        try:
            item = Coord.make(item)
        except SpreadsheetError as e:
            raise KeyError(e)
        if item in self.data:
            self.data[item].clear(self)
        self.data[item] = formula.make(value)

    def get(self, coord: Coord):
        if coord not in self.data:
            self.data[coord] = const(0)
        return self.data[coord]
