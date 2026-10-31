import numpy as np
import sub


def test_metropolis_symmetric_and_asymmetric():
    rng = np.random.default_rng(4)
    pi = rng.random(5) + 0.1
    pi /= pi.sum()
    sym = (np.ones((5, 5)) - np.eye(5)) / 4
    asym = rng.random((5, 5)) + 0.05
    asym /= asym.sum(axis=1, keepdims=True)
    for Q in (sym, asym):
        P = sub.metropolis_matrix(pi, Q)
        assert np.all(P >= -1e-15) and np.allclose(P.sum(axis=1), 1)
        assert sub.is_reversible(P, pi)
        assert np.allclose(pi @ P, pi)
        assert np.max(np.abs(np.imag(np.linalg.eigvals(P)))) < 1e-10


def test_stationary_without_balance():
    P = sub.cycle_chain(6, 0.7)
    u = np.ones(6) / 6
    assert np.allclose(u @ P, u)
    assert not sub.is_reversible(P, u)
    assert sub.is_reversible(sub.cycle_chain(6, 0.0), u)
