import numpy as np
import sub

EIGS = np.array([1.0, 2.0, 5.0, 20.0, 50.0])
A = sub.make_quadratic(EIGS, 6)
B = np.arange(5.0)
X0 = np.full(5, 3.0)


def test_spectrum():
    assert np.allclose(np.linalg.eigvalsh(A), EIGS)
    assert np.allclose(A, A.T)


def test_rates():
    L, mu = EIGS.max(), EIGS.min()
    for step, expected in ((1 / L, 1 - mu / L), (2 / (L + mu), (L - mu) / (L + mu))):
        assert abs(sub.rate(EIGS, step) - expected) < 1e-12
        e = sub.gd_errors(A, B, X0, step, 300)
        late = (e[-1] / e[-11]) ** 0.1
        assert abs(late - expected) < 2e-3, (late, expected)


def test_rotation_does_not_matter():
    D = np.diag(EIGS)
    rng = np.random.default_rng(7)
    Q = np.linalg.eigh(A)[1]
    x0, b = rng.normal(size=5), rng.normal(size=5)
    e1 = sub.gd_errors(A, b, x0, 0.02, 50)
    e2 = sub.gd_errors(D, Q.T @ b, Q.T @ x0, 0.02, 50)
    assert np.allclose(e1, e2, rtol=1e-8)
