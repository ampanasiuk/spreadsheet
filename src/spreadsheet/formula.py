from spreadsheet.cellvalues import cellvalues
from spreadsheet import Coord
from spreadsheet.coord import CoordLike


class formula:
    @staticmethod
    def make(obj):
        if isinstance(obj, formula):
            return obj
        if not isinstance(obj, int):
            raise TypeError
        return const(obj)

    def __add__(self, other):
        return sum(self, formula.make(other))

    def __radd__(self, other):
        return sum(formula.make(other), self)

    def __mul__(self, other):
        return mul(self, formula.make(other))

    def __rmul__(self, other):
        return mul(formula.make(other), self)

    def value(self, s: cellvalues):
        raise NotImplementedError


class const(formula):
    def __init__(self, val: int):
        self.val = val

    def value(self, s: cellvalues):
        return self.val


class ref(formula):
    def __init__(self, coord: CoordLike):
        if not isinstance(coord, Coord):
            coord = Coord(coord)
        self.coord = coord

    def value(self, s: cellvalues):
        return s.get(self.coord)


class sum(formula):
    def __init__(self, left: formula, right: formula):
        self.left = left
        self.right = right

    def value(self, s: cellvalues):
        return self.left.value(s) + self.right.value(s)


class mul(formula):
    def __init__(self, left: formula, right: formula):
        self.left = left
        self.right = right

    def value(self, s: cellvalues):
        return self.left.value(s) * self.right.value(s)
