import numpy as np
import sub


def test_diagonalizable():
    assert not sub.is_diagonalizable(np.array([[1.0, 1], [0, 1]]))
    assert sub.is_diagonalizable(np.array([[2.0, 1], [1, 2]]))
    assert sub.is_diagonalizable(np.array([[0.0, -1], [1, 0]]))
    assert sub.is_diagonalizable(np.array([[1.0, 1], [0, 1.001]]))


def test_slow_crawl():
    assert np.allclose(sub.shear_power(7), [[1, 7], [0, 1]])
    assert np.isclose(sub.angle_after(20), np.degrees(np.arctan(1 / 20)))
    assert 2.5 < sub.angle_after(20) < 3.0
