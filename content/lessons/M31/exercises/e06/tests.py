import numpy as np
import sub

XT = np.linspace(0.05, 0.95, 50)


def test_parts_add_up():
    d = sub.decompose(3, 400, np.random.default_rng(6), XT)
    total = d["bias2"] + d["variance"] + d["noise"]
    assert abs(total / d["test_mse"] - 1) < 0.05, d


def test_tradeoff():
    d1 = sub.decompose(1, 300, np.random.default_rng(7), XT)
    d3 = sub.decompose(3, 300, np.random.default_rng(8), XT)
    d5 = sub.decompose(5, 300, np.random.default_rng(10), XT)
    d9 = sub.decompose(9, 300, np.random.default_rng(9), XT)
    assert d1["bias2"] > d3["bias2"] > d5["bias2"]
    assert d3["variance"] < d5["variance"] < d9["variance"]
    assert d3["test_mse"] < min(d1["test_mse"], d9["test_mse"])
