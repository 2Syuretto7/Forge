import numpy as np
import sub


def test_matches_naive_formula_for_moderate_logits():
    a = np.linspace(-5, 5, 11)
    for y in (0.0, 1.0):
        s = 1 / (1 + np.exp(-a))
        naive = -(y * np.log(s) + (1 - y) * np.log(1 - s))
        assert np.allclose(sub.bce_with_logits(a, np.full_like(a, y)), naive, atol=1e-12)


def test_stable_at_extremes():
    v = sub.bce_with_logits(np.array([1000.0, -1000.0]), np.array([0.0, 1.0]))
    assert np.allclose(v, [1000.0, 1000.0])
    assert np.allclose(sub.bce_with_logits(np.array([50.0]), np.array([1.0])), np.exp(-50.0), rtol=1e-6)


def test_grad_matches_finite_differences():
    a = np.array([-2.0, -0.3, 0.0, 1.7])
    y = np.array([1.0, 0.0, 1.0, 0.0])
    g = sub.bce_grad(a, y)
    h = 1e-6
    num = (sub.bce_with_logits(a + h, y) - sub.bce_with_logits(a - h, y)) / (2 * h)
    assert np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num)) < 1e-5


def test_best_expected_loss_is_the_entropy():
    p = 0.3
    a = np.log(p / (1 - p))
    expected = p * sub.bce_with_logits(np.array([a]), np.array([1.0]))[0] + (1 - p) * sub.bce_with_logits(np.array([a]), np.array([0.0]))[0]
    assert abs(expected - sub.binary_entropy(p)) < 1e-12
    assert abs(sub.binary_entropy(0.5) - np.log(2)) < 1e-12 and sub.binary_entropy(0.0) == 0.0
