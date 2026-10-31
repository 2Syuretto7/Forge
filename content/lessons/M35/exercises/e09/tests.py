import numpy as np
import sub

TRUE = dict(E=1.69, A=406.4, alpha=0.34, B=410.7, beta=0.28)


def test_grad_surface():
    th = np.array([1.8, -1.2, 0.3, -0.9, 0.25])
    N, D = np.array([3e8, 2e9]), np.array([5e9, 4e10])
    J = sub.grad_surface(th, N, D)
    h = 1e-6
    for j in range(5):
        e = np.zeros(5)
        e[j] = h
        num = (sub.surface(th + e, N, D) - sub.surface(th - e, N, D)) / (2 * h)
        assert np.max(np.abs(num - J[:, j])) < 1e-7


def test_recovers_chinchilla():
    rng = np.random.default_rng(0)
    N, D = [a.ravel() for a in np.meshgrid(np.logspace(8, 9.5, 8), np.logspace(9, 11, 8))]
    L = TRUE["E"] + TRUE["A"] / N ** TRUE["alpha"] + TRUE["B"] / D ** TRUE["beta"] + 0.005 * rng.standard_normal(64)
    th = sub.fit_surface(N, D, L, [2.0, -1.0, 0.3, -1.0, 0.3])
    E, A, alpha, B, beta = sub.to_chinchilla(th)
    assert abs(alpha - 0.34) < 0.03 and abs(beta - 0.28) < 0.03 and abs(E - 1.69) < 0.1
