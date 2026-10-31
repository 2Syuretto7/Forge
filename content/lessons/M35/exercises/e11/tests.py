import math
import numpy as np
import sub

TRUE = (1.69, 406.4, 0.34, 410.7, 0.28)


def test_interval_widens():
    rng = np.random.default_rng(0)
    C = 10 ** rng.uniform(18, 20, 200)
    N = 10 ** rng.uniform(-0.6, 0.6, 200) * sub.optimal_N(TRUE, C)
    D = C / (6 * N)
    L = TRUE[0] + TRUE[1] / N ** TRUE[2] + TRUE[3] / D ** TRUE[4] + 0.005 * rng.standard_normal(200)
    s = sub.bootstrap_optimal_N(N, D, L, [1e19, 1e24], 40, rng)
    w = sub.log_interval_width(s)
    assert w[1] > 2 * w[0], w
    lo, hi = np.quantile(s[:, 1], [0.05, 0.95])
    assert lo - 0.2 < math.log(sub.optimal_N(TRUE, 1e24)) < hi + 0.2
