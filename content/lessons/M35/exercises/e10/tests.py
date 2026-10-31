import numpy as np
import sub

TRUE = (1.69, 406.4, 0.34, 410.7, 0.28)


def runs(rng, n=200):
    C = 10 ** rng.uniform(18, 21, n)
    N = 10 ** rng.uniform(-0.5, 0.5, n) * sub.optimal_N(TRUE, C)
    D = C / (6 * N)
    L = TRUE[0] + TRUE[1] / N ** TRUE[2] + TRUE[3] / D ** TRUE[4] + 0.005 * rng.standard_normal(n)
    return N, D, L


def test_frontier():
    N, D, L = runs(np.random.default_rng(0))
    chin = sub.fit_surface(N, D, L)
    assert abs(sub.frontier_exponent(chin) - 0.28 / 0.62) < 0.05
    for C in (1e20, 1e23):
        assert abs(sub.optimal_N_numeric(TRUE, C) / sub.optimal_N(TRUE, C) - 1) < 1e-4
    assert abs(sub.frontier_exponent(TRUE) - 0.4516) < 1e-3
