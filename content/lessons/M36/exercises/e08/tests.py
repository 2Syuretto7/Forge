import numpy as np
import sub


def test_grad_policy_gradient_theorem():
    rng = np.random.default_rng(0)
    S, A = 4, 3
    P = rng.random((A, S, S))
    P /= P.sum(axis=2, keepdims=True)
    R = rng.standard_normal((S, A))
    rho0 = np.array([0.5, 0.5, 0.0, 0.0])
    theta = rng.standard_normal((S, A))
    G = sub.policy_gradient(P, R, theta, rho0, 0.9)
    h = 1e-6
    for s in range(S):
        for a in range(A):
            E = np.zeros((S, A))
            E[s, a] = h
            num = (sub.objective(P, R, theta + E, rho0, 0.9) - sub.objective(P, R, theta - E, rho0, 0.9)) / (2 * h)
            assert abs(num - G[s, a]) < 1e-6
