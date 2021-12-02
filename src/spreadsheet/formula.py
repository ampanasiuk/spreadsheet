from spreadsheet import Coord
from spreadsheet.cellstorage import CellStorage
from spreadsheet.coord import CoordLike
from spreadsheet.listener import Listenable
from spreadsheet.listener import Listener
from spreadsheet.spreadsheet_error import SpreadsheetError


class formula(Listener, Listenable):
    def __init__(self):
        super().__init__()
        self.cached = None
        self.gray = False

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

    def value(self, s: CellStorage):
        if self.gray:
            raise SpreadsheetError("cycle")
        if self.cached is None:
            self.gray = True
            self.cached = self._value(s)
            self.gray = False
        return self.cached

    def clear(self, s: CellStorage):
        if self.gray:
            raise SpreadsheetError("cycle")
        self.gray = True
        if self.cached is not None:
            self.cached = None
            self.notify(s)
        self.gray = False

    def onevent(self, s: CellStorage):
        self.clear(s)

    def _value(self, s: CellStorage):
        raise NotImplementedError


class const(formula):
    def __init__(self, val: int):
        super().__init__()
        self.val = val

    def _value(self, s: CellStorage):
        return self.val

    def __repr__(self):
        return str(self.val)


class ref(formula):
    def __init__(self, coord: CoordLike):
        super().__init__()
        if not isinstance(coord, Coord):
            coord = Coord(coord)
        self.coord = coord

    def _value(self, s: CellStorage):
        s.get(self.coord).add_listener(self)
        return s.get(self.coord).value(s)

    def __repr__(self):
        return repr(self.coord)


class sum(formula):
    def __init__(self, left: formula, right: formula):
        super().__init__()
        self.left = left
        self.left.add_listener(self)
        self.right = right
        self.right.add_listener(self)

    def _value(self, s: CellStorage):
        return self.left.value(s) + self.right.value(s)

    def __repr__(self):
        return f"{self.left}+{self.right}"


class mul(formula):
    def __init__(self, left: formula, right: formula):
        super().__init__()
        self.left = left
        self.left.add_listener(self)
        self.right = right
        self.right.add_listener(self)

    def _value(self, s: CellStorage):
        return self.left.value(s) * self.right.value(s)

    def __repr__(self):
        return f"{self.left}*{self.right}"
