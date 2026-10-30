import math
import sub

calls = {"n": 0}


def counted(df):
    def wrapper(v):
        calls["n"] += 1
        return df(v)
    return wrapper


CHAIN = [
    (math.sin, math.cos),
    (lambda v: v * v + 1, lambda v: 2 * v),
    (math.log, lambda v: 1 / v),
    (math.exp, math.exp),
]


def exact(x):
    s = math.sin(x)
    u = s * s + 1
    return math.exp(math.log(u)), math.exp(math.log(u)) * (1 / u) * 2 * s * math.cos(x)


def test_forward_accumulation():
    v, d = sub.forward_accumulate(CHAIN, 0.7)
    ev, ed = exact(0.7)
    assert abs(v - ev) < 1e-12 and abs(d - ed) < 1e-12


def test_reverse_accumulation_matches_and_calls_each_derivative_once():
    chain = [(g, counted(dg)) for g, dg in CHAIN]
    calls["n"] = 0
    v, d = sub.reverse_accumulate(chain, 0.7)
    ev, ed = exact(0.7)
    assert abs(v - ev) < 1e-12 and abs(d - ed) < 1e-12
    assert calls["n"] == len(CHAIN)


def test_stored_values():
    s = sub.stored_values(CHAIN, 0.7)
    assert len(s) == 4
    assert abs(s[0] - 0.7) < 1e-15 and abs(s[1] - math.sin(0.7)) < 1e-15
