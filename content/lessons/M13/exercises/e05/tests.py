import numpy as np
import sub

rng = np.random.default_rng(5)


def test_invariant_weighted_average():
    for _ in range(200):
        n = int(rng.integers(1, 7))
        M = rng.normal(size=(n, n))
        S = M + M.T
        x = rng.normal(size=n)
        lam, w = sub.eig_weights(S, x)
        r = sub.rayleigh(S, x)
        assert np.all(w >= 0) and np.isclose(w.sum(), 1)
        assert np.isclose(r, lam @ w)
        assert lam.min() - 1e-12 <= r <= lam.max() + 1e-12
        assert np.isclose(sub.rayleigh(S, -2.5 * x), r)
