from spreadsheet import CoordLike


class formula:
    def __add__(self, other):
        raise NotImplementedError


class ref(formula):
    def __init__(self, coord: CoordLike):
        raise NotImplementedError
