import numpy as np
import sub

rng = np.random.default_rng(10)
counts = np.array([5.0, 0.0, 12.0, 3.0])


def test_softmax_properties():
    z = rng.normal(size=6)
    p = sub.softmax(z)
    assert abs(p.sum() - 1) < 1e-12 and np.all(p > 0)
    assert np.allclose(sub.softmax(z + 100.0), p), "softmax is shift invariant"
    big = sub.softmax(np.array([1000.0, 0.0]))
    assert np.all(np.isfinite(big)) and abs(big[0] - 1) < 1e-12


def test_nll_is_stable_and_correct():
    z = np.array([0.1, -0.3, 0.7, 0.0])
    p = np.exp(z) / np.exp(z).sum()
    assert abs(sub.nll(z, counts) + np.sum(counts * np.log(p))) < 1e-10
    assert np.isfinite(sub.nll(np.array([800.0, 0.0, 0.0, 0.0]), counts))


def test_grad_matches_finite_differences():
    z = rng.normal(size=4)
    g = sub.grad_nll(z, counts)
    num = np.zeros(4)
    for i in range(4):
        e = np.zeros(4)
        e[i] = 1e-6
        num[i] = (sub.nll(z + e, counts) - sub.nll(z - e, counts)) / 2e-6
    assert np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num)) < 1e-5


def test_gradient_zero_at_mle():
    c = np.array([4.0, 1.0, 5.0])
    p = sub.mle_probs(c)
    assert np.allclose(p, [0.4, 0.1, 0.5])
    assert np.linalg.norm(sub.grad_nll(np.log(p) + 3.0, c)) < 1e-10
