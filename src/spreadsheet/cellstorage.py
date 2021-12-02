from spreadsheet.coord import Coord


class CellStorage:
    def get(self, coord: Coord):
        raise NotImplementedError
