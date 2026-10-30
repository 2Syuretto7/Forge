import numpy as np
import sub

P = np.random.default_rng(0).normal(size=(1000, 2))


def test_quarter_turn_of_rows():
    X = np.array([[1.0, 0.0]]) @ sub.rotation(np.pi / 2, np.float64)
    assert np.allclose(X, [[0.0, 1.0]], atol=1e-15)


def test_float64_drift_is_tiny():
    d = sub.drift(P, 10000, np.float64)
    assert d < 1e-10, d


def test_float32_drift_is_visible():
    d32 = sub.drift(P, 10000, np.float32)
    assert 1e-5 < d32 < 1e-2, d32
    assert d32 > 1e6 * sub.drift(P, 10000, np.float64)
