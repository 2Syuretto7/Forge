import numpy as np
import sub

rng = np.random.default_rng(7)
Z = rng.normal(size=(6, 4)) * 3
y = rng.integers(0, 4, size=6)


def test_matches_direct_formula():
    P = np.exp(Z) / np.exp(Z).sum(axis=1, keepdims=True)
    ref = -np.mean(np.log(P[np.arange(6), y]))
    assert abs(sub.cross_entropy(Z, y) - ref) < 1e-12


def test_huge_logits_are_stable():
    big = np.array([[1000.0, 0.0, -1000.0], [-1000.0, -1001.0, -1002.0]])
    lse = sub.logsumexp(big)
    assert np.all(np.isfinite(lse))
    assert abs(lse[0] - 1000.0) < 1e-12
    assert np.isfinite(sub.cross_entropy(big, np.array([2, 0])))
    assert np.all(np.isfinite(sub.cross_entropy_grad(big, np.array([2, 0]))))


def test_grad_matches_finite_differences():
    G = sub.cross_entropy_grad(Z, y)
    num = np.zeros_like(Z)
    for idx in np.ndindex(Z.shape):
        E = np.zeros_like(Z)
        E[idx] = 1e-6
        num[idx] = (sub.cross_entropy(Z + E, y) - sub.cross_entropy(Z - E, y)) / 2e-6
    assert np.linalg.norm(G - num) / (np.linalg.norm(G) + np.linalg.norm(num)) < 1e-5


def test_gradient_rows_sum_to_zero():
    assert np.allclose(sub.cross_entropy_grad(Z, y).sum(axis=1), 0, atol=1e-15)
