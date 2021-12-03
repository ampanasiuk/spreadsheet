from spreadsheet import Spreadsheet
from spreadsheet.formula import ref


def test_usage():
    s = Spreadsheet()

    assert 0 == s["A1"]

    s["A1"] = 2
    assert 2 == s["A1"]

    s["A2"] = ref("A1") + 10
    assert 12 == s["A2"]

    s["A1"] = 5
    assert 15 == s["A2"]

    f = ref("A1") + ref("A2")
    s["B1"] = f
    s["B2"] = f + 1
    s["C1"] = f * 2
    assert 20 == s["B1"]
    assert 21 == s["B2"]
    assert 40 == s["C1"]
