import numpy as np
import sub


def test_tiny():
    naive, piv = sub.solve_both(1e-20)
    assert naive[0] == 0.0
    assert np.allclose(piv, [1, 1])


def test_digits():
    d_naive, d_piv = sub.digits(1e-8)
    assert 6 < d_naive < 10, d_naive
    assert d_piv > 15
    assert sub.digits(1e-20)[0] < 1
    assert sub.digits(0.5)[0] > 14
