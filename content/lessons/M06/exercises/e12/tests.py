import numpy as np
import sub

rng = np.random.default_rng(0)
X = np.linspace(1, 20, 40)


def test_exponential():
    y = 2.0 * 1.5 ** X * np.exp(rng.normal(scale=0.02, size=X.size))
    a, b = sub.fit_exponential(X, y)
    assert abs(a / 2 - 1) < 0.05 and abs(b / 1.5 - 1) < 0.01


def test_power():
    y = 3.0 * X ** 2.5 * np.exp(rng.normal(scale=0.02, size=X.size))
    c, p = sub.fit_power(X, y)
    assert abs(c / 3 - 1) < 0.05 and abs(p - 2.5) < 0.02
