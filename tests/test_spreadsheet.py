import pytest

from spreadsheet import Coord
from spreadsheet import Spreadsheet
from spreadsheet import SpreadsheetError
from spreadsheet.formula import ref
from spreadsheet.formula import cond


def test_spreadsheet_can_be_constructed():
    _ = Spreadsheet()


@pytest.fixture
def s():
    return Spreadsheet()


@pytest.mark.parametrize("coord", ["A1", "B8", "CD31"])
def test_cell_values_should_initially_be_zero(s, coord):
    assert 0 == s[coord]


@pytest.mark.parametrize("coord", ["A0", "A-1", "Ą1", "AAB", "a1", "ab", "156", "A1B", "A1!"])
def test_should_only_accept_chess_coords(s, coord):
    with pytest.raises(KeyError, match=r'invalid coord'):
        _ = s[coord]


@pytest.mark.parametrize("coord,value", [("A1", 1), ("CD3", 5), ("F34", -44)])
def test_should_be_possible_to_store_int(s, coord, value):
    s[coord] = value
    assert value == s[coord]
    # cell A2 should be affected
    assert 0 == s["A2"]


def test_should_be_possible_to_ref_cell(s):
    s["A2"] = 3
    s["A1"] = ref("A2")
    assert 3 == s["A1"]


def test_ref_should_update(s):
    s["B1"] = ref("A1")
    assert 0 == s["B1"]
    s["A1"] = 4
    assert 4 == s["B1"]
    s["A1"] = -7
    assert -7 == s["B1"]


def test_ref_should_follow_another_ref(s):
    s["C1"] = ref("B1")
    s["B1"] = ref("A1")
    assert 0 == s["C1"]
    s["A1"] = 9
    assert 9 == s["C1"]
    s["A1"] = -8
    assert -8 == s["C1"]


def test_formula_add_can_take_operands_ref_and_int(s):
    s["B1"] = ref("A1") + 1
    s["A1"] = 9
    assert 10 == s["B1"]
    s["A1"] = 11
    assert 12 == s["B1"]


def test_formula_add_can_take_operands_int_and_ref(s):
    s["D8"] = 1 + ref("A2")
    s["A2"] = 9
    assert 10 == s["D8"]
    s["A2"] = 11
    assert 12 == s["D8"]


def test_formula_add_can_take_operands_ref_and_ref_and_ref(s):
    s["A1"] = ref("A2") + ref("A3") + ref("A4")
    s["A2"] = 1
    s["A3"] = 10
    s["A4"] = 100
    assert 111 == s["A1"]


def test_formula_add_should_follow_refs(s):
    s["A1"] = ref("A2") + 1
    s["A2"] = ref("A3")
    s["A3"] = 10
    assert 11 == s["A1"]


def test_formula_mul_can_take_operands_ref_and_int(s):
    s["D8"] = ref("A2") * 2
    s["A2"] = 9
    assert 18 == s["D8"]
    s["A2"] = 11
    assert 22 == s["D8"]


def test_formula_mul_can_take_operands_int_and_ref(s):
    s["D8"] = 2 * ref("A2")
    s["A2"] = 9
    assert 18 == s["D8"]
    s["A2"] = 11
    assert 22 == s["D8"]


def test_formula_mul_add_can_be_combined(s):
    s["A1"] = (ref("A2") * 2 + 1) * ref("A3")
    s["A2"] = 10
    s["A3"] = 2
    assert 42 == s["A1"]


def test_formula_can_be_reused(s):
    form = ref("A1") + 10
    s["A2"] = form
    s["A3"] = form + 1
    s["A4"] = form + form
    s["A1"] = 2
    assert 12 == s["A2"]
    assert 13 == s["A3"]
    assert 24 == s["A4"]


def test_values_are_cached(s):
    s["A1"] = 1
    s["A2"] = ref("A1") + ref("A1") + ref("A1") + ref("A1") + ref("A1") + ref("A1") + ref("A1") + ref("A1")
    s["A3"] = ref("A2") + ref("A2") + ref("A2") + ref("A2") + ref("A2") + ref("A2") + ref("A2") + ref("A2")
    s["A4"] = ref("A3") + ref("A3") + ref("A3") + ref("A3") + ref("A3") + ref("A3") + ref("A3") + ref("A3")
    s["A5"] = ref("A4") + ref("A4") + ref("A4") + ref("A4") + ref("A4") + ref("A4") + ref("A4") + ref("A4")
    s["A6"] = ref("A5") + ref("A5") + ref("A5") + ref("A5") + ref("A5") + ref("A5") + ref("A5") + ref("A5")
    s["A7"] = ref("A6") + ref("A6") + ref("A6") + ref("A6") + ref("A6") + ref("A6") + ref("A6") + ref("A6")
    s["A8"] = ref("A7") + ref("A7") + ref("A7") + ref("A7") + ref("A7") + ref("A7") + ref("A7") + ref("A7")
    s["A9"] = ref("A8") + ref("A8") + ref("A8") + ref("A8") + ref("A8") + ref("A8") + ref("A8") + ref("A8")
    s["A10"] = ref("A9") + ref("A9") + ref("A9") + ref("A9") + ref("A9") + ref("A9") + ref("A9") + ref("A9")
    s["A11"] = ref("A10") + ref("A10") + ref("A10") + ref("A10") + ref("A10") + ref("A10") + ref("A10") + ref("A10")
    s["A12"] = ref("A11") + ref("A11") + ref("A11") + ref("A11") + ref("A11") + ref("A11") + ref("A11") + ref("A11")
    s["A13"] = ref("A12") + ref("A12") + ref("A12") + ref("A12") + ref("A12") + ref("A12") + ref("A12") + ref("A12")
    s["A14"] = ref("A13") + ref("A13") + ref("A13") + ref("A13") + ref("A13") + ref("A13") + ref("A13") + ref("A13")
    s["A15"] = ref("A14") + ref("A14") + ref("A14") + ref("A14") + ref("A14") + ref("A14") + ref("A14") + ref("A14")
    s["A16"] = ref("A15") + ref("A15") + ref("A15") + ref("A15") + ref("A15") + ref("A15") + ref("A15") + ref("A15")
    s["A17"] = ref("A16") + ref("A16") + ref("A16") + ref("A16") + ref("A16") + ref("A16") + ref("A16") + ref("A16")
    assert 281474976710656 == s["A17"]


def test_diamond_should_recalc(s):
    root = Coord("A1")
    l = Coord("B1")
    r = Coord("B2")
    b = Coord("C1")
    s[b] = ref(l) + ref(r)
    s[l] = ref(root)
    s[r] = ref(root) * 10
    s[root] = 2
    assert 22 == s[b]
    s[root] = 3
    assert 33 == s[b]


def test_uneven_diamond_should_recalc(s):
    root = Coord("A1")
    l = Coord("B1")
    r1 = Coord("B2")
    r2 = Coord("C2")
    b = Coord("D1")
    s[b] = ref(l) + ref(r2)
    s[l] = ref(root)
    s[r2] = ref(r1)
    s[r1] = ref(root) * 10
    s[root] = 2
    assert 22 == s[b]
    s[root] = 3
    assert 33 == s[b]


def test_cycles_should_raise(s):
    s["A1"] = ref("A1")
    with pytest.raises(SpreadsheetError, match=r"cycle"):
        _ = s["A1"]


@pytest.mark.parametrize("coord", ["A1", "A2", "A3"])
def test_cycles_len_3_should_raise(s, coord):
    s["A1"] = ref("A3")
    s["A2"] = ref("A1")
    s["A3"] = ref("A2")
    with pytest.raises(SpreadsheetError, match=r"cycle"):
        _ = s[coord]


@pytest.mark.parametrize("condition", [1, 2, -1])
def test_truish_condition_should_evaluate_to_then_val(s, condition):
    s["A1"] = cond(condition, 2, 3)
    assert 2 == s["A1"]


def test_false_condition_should_evaluate_to_else_val(s):
    s["A1"] = cond(0, 2, 3)
    assert 3 == s["A1"]
