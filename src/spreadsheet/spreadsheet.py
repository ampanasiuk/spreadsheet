from typing import Dict

from spreadsheet.cellvalues import cellvalues
from spreadsheet.coord import Coord
from spreadsheet.coord import CoordLike
from spreadsheet.formula import formula
from spreadsheet.spreadsheet_error import SpreadsheetError


class Spreadsheet(cellvalues):
    def __init__(self):
        self.data: Dict[Coord, formula] = {}

    def __getitem__(self, item):
        if not isinstance(item, CoordLike):
            raise TypeError
        try:
            item = Coord.make(item)
        except SpreadsheetError as e:
            raise KeyError(e)
        return self.get(item)

    def __setitem__(self, item, value):
        if not isinstance(item, CoordLike):
            raise TypeError
        try:
            item = Coord.make(item)
        except SpreadsheetError as e:
            raise KeyError(e)
        self.data[item] = formula.make(value)

    def get(self, coord: Coord):
        if coord in self.data:
            return self.data[coord].value(self)
        return 0
