from spreadsheet import CoordLike


class formula:
    def __add__(self, other):
        raise NotImplementedError

    def __radd__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError

    def __rmul__(self, other):
        raise NotImplementedError


class ref(formula):
    def __init__(self, coord: CoordLike):
        raise NotImplementedError
