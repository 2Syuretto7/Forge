import numpy as np
import sub


def test_order_drops():
    ns = np.array([2 ** k + 2 for k in range(3, 14)])
    ns = ns[ns % 3 != 0]
    errs = sub.simpson_step_errors(ns)
    p = sub.fitted_order(ns, errs)
    assert 0.5 < p < 1.5, p


def test_split():
    assert sub.split_at_jump(10) < 1e-15
