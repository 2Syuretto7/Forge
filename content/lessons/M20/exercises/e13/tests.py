import numpy as np
import sub


def test_one_dimension():
    assert abs(sub.total(sub.wrong_density) - 2) < 1e-6
    assert abs(sub.total(sub.right_density) - 1) < 1e-6


def test_two_dimensions():
    A = np.array([[2.0, 0.5], [-0.3, 1.5]])
    xs = np.linspace(-15, 15, 301)
    h = xs[1] - xs[0]
    tot = sum(sub.linear_density(np.array([a, b]), A) for a in xs for b in xs) * h * h
    assert abs(tot - 1) < 1e-4
