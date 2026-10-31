import math
import numpy as np
import sub

EPS = 2.0**-52


def test_scalar():
    assert abs(sub.scalar_condition(math.log, lambda x: 1 / x, 1.001) - 1 / math.log(1.001)) < 1e-6
    assert abs(sub.scalar_condition(math.sqrt, lambda x: 0.5 / math.sqrt(x), 7.0) - 0.5) < 1e-12
    assert sub.scalar_condition(lambda x: x - 1, lambda x: 1.0, 1.000001) > 1e5


def test_hilbert():
    assert np.allclose(sub.hilbert(3), [[1, 1 / 2, 1 / 3], [1 / 2, 1 / 3, 1 / 4], [1 / 3, 1 / 4, 1 / 5]])
    k = [sub.matrix_condition(sub.hilbert(n)) for n in (4, 8, 12)]
    assert 1e4 < k[0] < 3e4 and 1e10 < k[1] < 3e10 and k[2] > 1e15


def test_error_tracks_condition():
    for n in range(2, 13):
        err, kappa = sub.solve_error(n)
        assert err < 10 * kappa * EPS, (n, err, kappa)
    err12, _ = sub.solve_error(12)
    err4, _ = sub.solve_error(4)
    assert err12 > 1e-6 and err4 < 1e-11
