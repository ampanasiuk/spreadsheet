from typing import Dict

from spreadsheet.coord import Coord
from spreadsheet.cellvalues import cellvalues
from spreadsheet.formula import formula


class SpreadsheetError(Exception):
    pass


class Spreadsheet(cellvalues):
    def __init__(self):
        self.data: Dict[Coord, formula] = {}

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError
        if isinstance(item, str):
            try:
                item = Coord(item)
            except SpreadsheetError as e:
                raise KeyError(e)
        return self.get(item)

    def get(self, coord: Coord):
        if coord in self.data:
            return self.data[coord].value(self)
        return 0
