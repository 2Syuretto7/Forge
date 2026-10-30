import numpy as np
import sub


def test_fraction_is_about_two_t():
    f = sub.fraction_small_det(10000, 0.01)
    assert 0.012 < f < 0.03, f
    assert sub.fraction_small_det(10000, 0.1) > sub.fraction_small_det(10000, 0.01)


def test_amplification():
    easy = sub.amplification(np.array([[1.0, 0.0], [0.0, 1.0]]), np.array([1.0, 2.0]))
    assert abs(easy - 1) < 1e-6
    hard = sub.amplification(np.array([[1.0, 1.0], [1.0, 1.0001]]), np.array([2.0, 2.0001]))
    assert hard > 1e4, f"nearly parallel lines should amplify a nudge by over 10,000, got {hard:.3g}"
