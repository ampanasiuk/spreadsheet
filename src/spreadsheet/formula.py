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
    """
    A formula

    Note: a formula should not be tied by inputs or assignment to more than one spreadsheet.
    """
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

    def __lt__(self, other):
        return lt(self, formula.make(other))

    def __le__(self, other):
        return le(self, formula.make(other))

    def __gt__(self, other):
        return gt(self, formula.make(other))

    def __ge__(self, other):
        return ge(self, formula.make(other))

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
    def __init__(self, operands: List[formula], op: Callable[..., int]):
        super().__init__()
        self.op = op
        self.operands = tuple(operands)
        for operand in self.operands:
            operand.add_listener(self)

    def _value(self, s: CellStorage):
        return self.op(*[operand.value(s) for operand in self.operands])


class binary_op(op):
    def __init__(self, symbol: str, left: formula, right: formula, op: Callable[[int, int], int]):
        super().__init__([left, right], op)
        self.symbol = symbol

    def __repr__(self):
        return self.symbol.join(map(repr, self.operands))


sum = lambda l, r: binary_op("+", l, r, operator.add)
mul = lambda l, r: binary_op("*", l, r, operator.mul)
lt = lambda l, r: binary_op("<", l, r, lambda l, r: 0 + operator.lt(l, r))
le = lambda l, r: binary_op("<=", l, r, lambda l, r: 0 + operator.le(l, r))
gt = lambda l, r: binary_op(">", l, r, lambda l, r: 0 + operator.gt(l, r))
ge = lambda l, r: binary_op(">=", l, r, lambda l, r: 0 + operator.ge(l, r))


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
