import numpy as np
import sub

HILL = lambda x: np.exp(-x * x)


def test_error_falls():
    errs = sub.error_table(HILL, -3, 3, [10, 100, 1000])
    assert errs[0] > errs[1] > errs[2]
    assert 50 < errs[0] / errs[1] < 200, "ten times the pieces, about a hundred times smaller"


def test_factor_of_four():
    errs = sub.error_table(HILL, -3, 3, [10, 20, 40, 80, 160])
    for r in sub.shrink_factors(errs):
        assert 3.0 < r < 5.0, r


def test_sine():
    errs = sub.error_table(np.sin, 0, 2 * np.pi, [16, 32, 64])
    assert all(3.0 < r < 5.0 for r in sub.shrink_factors(errs))
