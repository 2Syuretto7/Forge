import numpy as np
import sub


def test_estimators_on_known_sample():
    b, u = sub.variance_estimators(np.array([1.0, 2.0, 3.0, 4.0]))
    assert abs(b - 1.25) < 1e-12 and abs(u - 5 / 3) < 1e-12


def test_bias_matches_theory():
    n, sigma = 5, 2.0
    b, u = sub.simulate_bias(n, sigma, 200000, seed=7)
    se = sigma ** 2 * np.sqrt(2 / (n - 1)) / np.sqrt(200000)  # standard error of the average
    assert abs(b - (-sigma ** 2 / n)) < 5 * se, f"biased: {b:.4f}, theory {-sigma**2/n:.4f}"
    assert abs(u) < 5 * se, f"unbiased: {u:.4f}"


def test_bias_shrinks_with_n():
    b5, _ = sub.simulate_bias(5, 1.0, 100000, seed=1)
    b50, _ = sub.simulate_bias(50, 1.0, 100000, seed=1)
    assert abs(b50) < abs(b5) / 4
