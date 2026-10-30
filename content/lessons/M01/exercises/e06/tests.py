import math
import sub


def test_convert():
    assert abs(sub.convert(2, "h", "s") - 7200) < 1e-9
    assert abs(sub.convert(1, "day", "min") - 1440) < 1e-9
    assert abs(sub.convert(14e9, "B", "GB") - 14) < 1e-12
    assert abs(sub.convert(14e9, "B", "GiB") - 13.0385160446167) < 1e-9


def test_dimensions_must_match():
    try:
        sub.convert(1, "h", "GB")
    except ValueError:
        return
    raise AssertionError("hours to gigabytes should raise ValueError")


def test_percent_bigger():
    assert abs(sub.percent_bigger("GiB", "GB") - 7.3741824) < 1e-6
    assert abs(sub.percent_bigger("TiB", "TB") - 9.9511627776) < 1e-6
    assert abs(sub.percent_bigger("h", "min") - 5900) < 1e-9


def test_best_unit():
    assert sub.best_unit(7200, "s") == (2.0, "h")
    assert sub.best_unit(0.5, "s") == (0.5, "s")
    n, u = sub.best_unit(3e18, "FLOP")
    assert u == "PFLOP" and abs(n - 3000) < 1e-6


def test_invariant_round_trip():
    for a, (da, _) in sub.UNITS.items():
        for b, (db, _) in sub.UNITS.items():
            if da == db:
                assert math.isclose(sub.convert(sub.convert(123.456, a, b), b, a), 123.456, rel_tol=1e-12), (a, b)
