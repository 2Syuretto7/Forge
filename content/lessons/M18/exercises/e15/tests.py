import numpy as np
import sub


def test_grad_kink_breaks_check():
    x = np.array([0.5, -0.3, 2e-7, 1.0])
    assert sub.check_at(x) > 0.1
    assert sub.check_at(sub.safe_point(x)) < 1e-8


def test_safe_point():
    s = sub.safe_point(np.array([0.0, -1e-9, 3.0]))
    assert np.isclose(s[0], 1e-5) and np.isclose(s[1], -1e-5) and s[2] == 3.0
