import numpy as np
import sub

rng = np.random.default_rng(9)
A = rng.normal(size=(4, 4))
S = A @ A.T + np.eye(4)
MU = np.array([0.5, -1.0, 2.0, 0.0])


def test_grad_conditional_mean_slope():
    obs = [1, 3]
    x0 = np.array([0.3, -0.7])
    B = sub.regression_slope(MU, S, obs)
    h = 1e-6
    for k in range(2):
        e = np.zeros(2)
        e[k] = h
        num = (sub.condition(MU, S, obs, x0 + e)[0] - sub.condition(MU, S, obs, x0 - e)[0]) / (2 * h)
        assert np.allclose(num, B[:, k], rtol=1e-6, atol=1e-8)


def test_bivariate():
    sx, sy, rho = 2.0, 1.5, 0.6
    C = np.array([[sx * sx, rho * sx * sy], [rho * sx * sy, sy * sy]])
    m, V = sub.condition(np.array([1.0, 3.0]), C, [0], [2.0])
    assert abs(m[0] - (3 + rho * sy / sx * 1.0)) < 1e-12
    assert abs(V[0, 0] - sy * sy * (1 - rho * rho)) < 1e-12


def test_by_rejection_sampling():
    C = np.array([[1.0, 0.8], [0.8, 1.0]])
    X = np.random.default_rng(10).standard_normal((400000, 2)) @ np.linalg.cholesky(C).T
    keep = X[np.abs(X[:, 0] - 1.0) < 0.02, 1]
    m, V = sub.condition(np.zeros(2), C, [0], [1.0])
    assert abs(keep.mean() - m[0]) < 0.03 and abs(keep.var() - V[0, 0]) < 0.03


def test_conditioning_never_increases_variance():
    _, V = sub.condition(MU, S, [2], [1.0])
    rest = [0, 1, 3]
    assert np.linalg.eigvalsh(S[np.ix_(rest, rest)] - V).min() > -1e-10
