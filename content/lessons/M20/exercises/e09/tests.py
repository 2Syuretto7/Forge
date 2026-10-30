import math
import numpy as np
import sub

S = np.array([[2.0, 0.8], [0.8, 1.0]])


def test_normalizers():
    assert abs(sub.normalizer(np.eye(3)) - (2 * math.pi) ** 1.5) < 1e-12
    assert abs(sub.normalizer(np.diag([4.0, 9.0])) - 12 * math.pi) < 1e-12


def test_integrates_to_one():
    xs = np.linspace(-8, 8, 321)
    h = xs[1] - xs[0]
    total = sum(sub.gaussian_density(np.array([a, b]), S) for a in xs for b in xs) * h * h
    assert abs(total - 1) < 1e-6


def test_samples():
    X = sub.sample_gaussian(S, 200_000)
    assert np.allclose(np.cov(X, rowvar=False), S, atol=0.02)
