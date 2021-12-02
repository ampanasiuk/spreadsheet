import operator
from typing import Callable
from typing import List

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


class op(formula):
    def __init__(self, operands: List[formula], op: Callable[[List[int]], int]):
        super().__init__()
        self.op = op
        self.operands = operands
        for operand in self.operands:
            operand.add_listener(self)

    def _value(self, s: CellStorage):
        return self.op(*[operand.value(s) for operand in self.operands])


class sum(op):
    def __init__(self, left: formula, right: formula):
        super().__init__([left, right], operator.add)

    def __repr__(self):
        return "+".join(map(repr, self.operands))


class mul(op):
    def __init__(self, left: formula, right: formula):
        super().__init__([left, right], operator.mul)

    def __repr__(self):
        return "*".join(map(repr, self.operands))


class cond(formula):
    def __init__(self, condition, then_val, else_val):
        super().__init__()
        self.condition = formula.make(condition)
        self.condition.add_listener(self)
        self.then_val = formula.make(then_val)
        self.then_val.add_listener(self)
        self.else_val = formula.make(else_val)
        self.else_val.add_listener(self)

    def _value(self, s: CellStorage):
        return self.then_val.value(s) if self.condition.value(s) else self.else_val.value(s)
