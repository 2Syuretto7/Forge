import numpy as np
import sub


def test_decomposition_adds_up():
    r = sub.bias_variance(3, 20, 0.3, 0.5, trials=6000, seed=1)
    total = r["bias2"] + r["variance"] + r["noise"]
    assert abs(total - r["expected_error"]) < 0.06 * total, r


def test_bias_falls_and_variance_rises_with_degree():
    lo = sub.bias_variance(1, 20, 0.3, 0.5, trials=3000, seed=2)
    hi = sub.bias_variance(9, 20, 0.3, 0.5, trials=3000, seed=2)
    assert lo["bias2"] > 10 * hi["bias2"]
    assert hi["variance"] > 3 * lo["variance"]
    assert abs(lo["noise"] - 0.09) < 1e-12
