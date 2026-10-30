import numpy as np
import sub

f = lambda x: np.sum(np.sin(x) * x)  # noqa: E731
good = lambda x: np.cos(x) * x + np.sin(x)  # noqa: E731
bad = lambda x: (np.cos(x) * x + np.sin(x)) * 1.001  # noqa: E731
X = np.random.default_rng(13).normal(size=8)


def test_grad_float32_too_loose():
    ok_good, _ = sub.check(f, good, X, np.float32, 1e-3, 1e-2)
    ok_bad, _ = sub.check(f, bad, X, np.float32, 1e-3, 1e-2)
    assert ok_good and ok_bad, "in float32 the bug hides below the tolerance"


def test_grad_float64_catches_it():
    ok_good, e_good = sub.check(f, good, X, np.float64, 1e-6, 1e-6)
    ok_bad, e_bad = sub.check(f, bad, X, np.float64, 1e-6, 1e-6)
    assert ok_good and not ok_bad, (e_good, e_bad)


def test_floor():
    assert 1e-6 < sub.float32_noise_floor(f, X, 1e-3) < 1e-2
