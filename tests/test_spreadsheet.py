import pytest

from spreadsheet import Spreadsheet
from spreadsheet import SpreadsheetError
from spreadsheet.formula import ref


def test_spreadsheet_can_be_constructed():
    s = Spreadsheet()


@pytest.fixture
def s():
    return Spreadsheet()


@pytest.mark.parametrize("coord", ["A1", "B8", "CD31"])
def test_cell_values_should_initially_be_zero(s, coord):
    assert 0 == s[coord]


@pytest.mark.parametrize("coord", ["a1", "ab", "156", "A1B", "A1!"])
def test_should_only_accept_chess_coords(s, coord):
    with pytest.raises(SpreadsheetError, matches=r'invalid coord'):
        _ = s[coord]


@pytest.mark.parametrize("coord,value", [("A1", 1), ("CD3", 5), ("F34", -44)])
def test_should_be_possible_to_store_int(s, coord, value):
    s[coord] = value
    assert value == s[coord]
    # cell A2 should be affected
    assert 0 == s["A2"]


def test_should_be_possible_to_ref_cell(s):
    s["A2"] = 3
    s["B3"] = ref("A2")
    assert 3 == s["B3"]


def test_ref_should_update(s):
    s["B3"] = ref("A2")
    assert 0 == s["B3"]
    s["A2"] = 4
    assert 4 == s["B3"]
    s["A2"] = -7
    assert -7 == s["B3"]


def test_ref_should_follow_another_ref(s):
    s["B3"] = ref("A2")
    s["A2"] = ref("C4")
    assert 0 == s["B3"]
    s["C4"] = 9
    assert 9 == s["B3"]
    s["C4"] = -8
    assert -8 == s["B3"]


def test_formula_sum_can_take_operands_ref_and_int(s):
    s["D8"] = ref("A2") + 1
    s["A2"] = 9
    assert 10 == s["D8"]
    s["A2"] = 11
    assert 12 == s["D8"]


def test_formula_sum_can_take_operands_ref_and_ref_and_ref(s):
    s["A1"] = ref("A2") + ref("A3") + ref("A4")
    s["A2"] = 1
    s["A3"] = 10
    s["A4"] = 100
    assert 111 == s["A1"]


def test_formula_sum_should_follow_refs(s):
    s["A1"] = ref("A2") + 1
    s["A2"] = ref("A3")
    s["A3"] = 10
    assert 11 == s["A1"]


def test_formula_can_be_reused(s):
    form = ref("A1") + 10
    s["A2"] = form
    s["A3"] = form + 1
    s["A4"] = form + form
    s["A1"] = 2
    assert 12 == s["A2"]
    assert 13 == s["A3"]
    assert 24 == s["A4"]
