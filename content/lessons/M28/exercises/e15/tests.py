import numpy as np
import sub

softplus = lambda u: np.maximum(u, 0) + np.log1p(np.exp(-np.abs(u)))


def test_rules():
    square = lambda x: x * x
    f1 = sub.compose(np.exp, square)
    assert sub.is_nondecreasing(np.exp, 0, 4) and sub.second_difference_min(f1, -2, 2) > 0
    f2 = sub.compose(square, lambda x: x * x - 1)
    assert not sub.is_nondecreasing(square, -1, 3)
    assert sub.second_difference_min(f2, -2, 2) < 0
    f3 = sub.compose(softplus, lambda x: 3 * x - 1)
    assert sub.second_difference_min(f3, -2, 2) > -1e-12


def test_compose():
    assert sub.compose(np.sqrt, np.abs)(-4.0) == 2.0
