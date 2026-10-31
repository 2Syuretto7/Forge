import math
import numpy as np
import sub


def test_square_root_of_kappa():
    rng = np.random.default_rng(0)
    its = {}
    for kappa in (10, 100, 1000, 10000):
        A = sub.spd_with_spectrum(np.geomspace(1, kappa, 300), rng)
        its[kappa] = sub.cg_iterations(A, rng.standard_normal(300))
        assert its[kappa] <= sub.iterations_predicted(kappa, 1e-8)
    assert 2.0 < its[10000] / its[100] < 12, its
    assert sub.iterations_predicted(10000, 1e-8) == math.ceil(math.log(1e-8 / 2) / math.log(99 / 101))


def test_few_distinct_eigenvalues():
    rng = np.random.default_rng(1)
    A = sub.spd_with_spectrum(np.repeat([1.0, 2.0, 5.0, 10.0, 50.0], 40), rng)
    assert sub.cg_iterations(A, rng.standard_normal(200), 1e-10) == 5
