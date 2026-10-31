import numpy as np
import sub


def mdp(seed, S=5, A=3):
    rng = np.random.default_rng(seed)
    P = rng.random((A, S, S))
    P /= P.sum(axis=2, keepdims=True)
    R = rng.standard_normal((S, A))
    pi = rng.random((S, A))
    return P, R, pi / pi.sum(axis=1, keepdims=True)


def test_bellman():
    P, R, pi = mdp(0)
    V = sub.policy_evaluation(P, R, pi, 0.9)
    Ppi, Rpi = sub.chain_of(P, R, pi)
    assert np.allclose(V, Rpi + 0.9 * Ppi @ V)
    mc = sub.mc_value(P, R, pi, 0.9, 2, 2000, 60, np.random.default_rng(1))
    assert abs(mc - V[2]) < 0.1, (mc, V[2])
    assert abs(sub.discounted_return([1, 1, 1], 0.5) - 1.75) < 1e-12
