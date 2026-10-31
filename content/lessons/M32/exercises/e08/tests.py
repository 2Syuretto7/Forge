import numpy as np
import sub


def test_autocorr():
    x = sub.ar1(0.9, 100000, np.random.default_rng(0))
    ac = sub.autocorr(x, 3)
    assert ac[0] == 1.0
    for k in (1, 2, 3):
        assert abs(ac[k] - 0.9**k) < 0.03


def test_ess():
    for phi in (0.5, 0.9):
        n = 50000
        e = sub.ess(sub.ar1(phi, n, np.random.default_rng(1)))
        assert abs(e / (n * (1 - phi) / (1 + phi)) - 1) < 0.12, (phi, e)
    iid = np.random.default_rng(2).standard_normal(20000)
    assert abs(sub.ess(iid) / 20000 - 1) < 0.1


def test_mcse_predicts_spread():
    rng = np.random.default_rng(3)
    chains = [sub.ar1(0.9, 2000, rng) for _ in range(200)]
    spread = np.std([c.mean() for c in chains])
    predicted = np.mean([sub.mcse(c) for c in chains])
    assert 0.8 < predicted / spread < 1.25, (predicted, spread)
