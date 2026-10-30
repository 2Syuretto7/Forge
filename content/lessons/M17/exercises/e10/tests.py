import math
import numpy as np
import sub


def test_exact():
    f = lambda x: np.exp(-2 * x) * np.cos(7 * x)  # noqa: E731
    x = np.linspace(0, 1, 200001)
    y = f(x)
    approx = (y.sum() - (y[0] + y[-1]) / 2) / 200000
    assert abs(sub.exact(2, 7) - approx) < 1e-9


def test_survey():
    t, s, a = sub.survey(200)
    assert s < t / 5, (t, s)
    assert a < 3 * s, (s, a)
