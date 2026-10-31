import numpy as np
import sub

PI = np.array([0.4, 0.3, 0.2, 0.1])
R = np.array([0.0, 1.0, -0.5, 2.0])


def test_grad_stationary_on_the_simplex():
    p = sub.kl_optimum(PI, R, 0.5)
    h = 1e-6
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            d = np.zeros(4)
            d[i], d[j] = h, -h
            num = (sub.kl_objective(p + d, PI, R, 0.5) - sub.kl_objective(p - d, PI, R, 0.5)) / (2 * h)
            assert abs(num) < 1e-6


def test_beats_random_and_recovers_reward():
    rng = np.random.default_rng(9)
    for beta in (0.2, 1.0, 5.0):
        p = sub.kl_optimum(PI, R, beta)
        best = sub.kl_objective(p, PI, R, beta)
        for _ in range(100):
            assert sub.kl_objective(rng.dirichlet(np.ones(4)), PI, R, beta) <= best + 1e-12
        rec = sub.implied_reward(p, PI, beta)
        assert np.allclose(rec - rec.mean(), R - R.mean())
    assert np.allclose(sub.kl_optimum(PI, R, 1e6), PI, atol=1e-5)
