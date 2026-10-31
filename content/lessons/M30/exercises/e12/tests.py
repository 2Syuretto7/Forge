import numpy as np
import sub

N = sub.make_noise()


def test_budget_and_kkt():
    nu = sub.water_level(N, 5000.0)
    x = sub.allocation(N, nu)
    assert abs(x.sum() - 5000.0) < 1e-9 * 5000
    assert sub.kkt_check(N, x, nu) < 1e-9
    assert 0 < np.mean(x > 0) < 1


def test_small_example():
    nu = sub.water_level([1.0, 2.0, 4.0], 2.0)
    assert abs(nu - 2.5) < 1e-12
    assert np.allclose(sub.allocation([1.0, 2.0, 4.0], nu), [1.5, 0.5, 0.0])
