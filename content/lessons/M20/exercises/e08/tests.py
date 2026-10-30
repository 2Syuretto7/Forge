import math
import numpy as np
import sub


def test_quantiles():
    e = sub.sample_exponential(200_000, 2.0)
    assert abs(np.median(e) - math.log(2) / 2) < 0.01
    c = sub.sample_cauchy(200_000)
    assert abs(np.quantile(c, 0.25) + 1) < 0.02 and abs(np.quantile(c, 0.75) - 1) < 0.02


def test_table():
    xs = np.linspace(0, 1, 2001)
    s = sub.sample_from_table(xs, 3 * xs ** 2 - 2 * xs ** 3, 200_000)
    assert abs(np.mean((s > 0.2) & (s < 0.3)) - 0.112) < 0.005
    assert abs(np.mean(s) - 0.5) < 0.005
