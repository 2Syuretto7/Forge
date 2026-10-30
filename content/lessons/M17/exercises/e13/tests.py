import numpy as np
import sub


def test_half_order():
    ns = np.array([10, 100, 1000, 10000, 100000])
    errs = sub.midpoint_errors(ns)
    assert abs(sub.fitted_order(ns, errs) - 0.5) < 0.05
    assert errs[-1] > 1e-3


def test_substitution():
    assert sub.after_substitution(10) < 1e-14
