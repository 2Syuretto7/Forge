import numpy as np
import sub

rng = np.random.default_rng(7)
z = rng.normal(size=6)


def test_grad_softmax_jacobian_matches_finite_differences():
    J = sub.softmax_jacobian(z)
    num = np.zeros((6, 6))
    for j in range(6):
        e = np.zeros(6)
        e[j] = 1e-6
        num[:, j] = (sub.softmax(z + e) - sub.softmax(z - e)) / 2e-6
    assert np.linalg.norm(J - num) / (np.linalg.norm(J) + np.linalg.norm(num)) < 1e-5


def test_jacobian_structure():
    J = sub.softmax_jacobian(z)
    assert np.allclose(J, J.T), "symmetric"
    assert np.allclose(J.sum(axis=0), 0, atol=1e-15), "columns sum to zero: shift invariance"
    w = np.linalg.eigvalsh(J)
    assert w.min() > -1e-12, "positive semidefinite"


def test_vjp_without_the_matrix():
    u = rng.normal(size=6)
    assert np.allclose(sub.softmax_vjp(z, u), u @ sub.softmax_jacobian(z))


def test_vjp_is_stable_for_huge_logits():
    big = np.array([1000.0, 999.0, -1000.0])
    v = sub.softmax_vjp(big, np.array([1.0, 0.0, 0.0]))
    assert np.all(np.isfinite(v))
