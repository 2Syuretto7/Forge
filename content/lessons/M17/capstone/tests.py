import math
import sub

REP = sub.report()


def test_all_twenty():
    assert len(REP) == 20
    for name, v, err, n in REP:
        assert err < 1e-8, f"{name}: error {err:.2e}"


def test_cost():
    assert sum(n for *_, n in REP) < 300_000


def test_transformations():
    spec = {"f": lambda x: math.exp(-x), "a": 0.0, "b": math.inf, "singular": False}
    (g, lo, hi), = sub.transformed(spec)
    assert (lo, hi) == (0.0, 1.0) and g(1.0) == 0.0
    spec = {"f": lambda x: x ** -0.5, "a": 0.0, "b": 4.0, "singular": True}
    (g, lo, hi), = sub.transformed(spec)
    assert hi == 2.0 and abs(g(0.0) - 2) < 1e-9
