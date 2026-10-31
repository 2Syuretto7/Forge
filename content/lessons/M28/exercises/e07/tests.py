import numpy as np
import sub


def test_bound_values():
    assert sub.iterations_bound(100, 1e-6) == 691
    assert sub.iterations_bound(100, 1e-6, "inverse_L") == 1375
    assert sub.iterations_bound(1.0001, 1e-6) == 2


def test_bound_holds_and_is_tight():
    for kappa in (10, 100, 1000):
        D = np.diag(np.linspace(1, kappa, 8))
        x0 = np.ones(8)
        k = sub.iterations_needed(D, np.zeros(8), x0, 2 / (kappa + 1), 1e-6)
        bound = sub.iterations_bound(kappa, 1e-6)
        assert k <= bound and k > 0.85 * bound, (kappa, k, bound)


def test_linear_in_kappa():
    ks = []
    for kappa in (30, 300):
        D = np.diag([1.0, kappa])
        ks.append(sub.iterations_needed(D, np.zeros(2), np.ones(2), 1 / kappa, 1e-6))
    assert 9 < ks[1] / ks[0] < 11
