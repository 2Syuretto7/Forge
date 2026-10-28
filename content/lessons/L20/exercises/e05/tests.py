import numpy as np
import sub

rng = np.random.default_rng(3)
M = rng.normal(size=(8, 3)) @ rng.normal(size=(3, 10)) + 0.01 * rng.normal(size=(8, 10))


def test_eckart_young():
    for r in [1, 2, 3]:
        best = sub.best_rank_r(M, r)
        assert np.linalg.matrix_rank(best) == r
        err = np.linalg.norm(M - best) / np.linalg.norm(M)
        assert abs(err - sub.relative_error(M, r)) < 1e-12
        other = rng.normal(size=(8, r)) @ rng.normal(size=(r, 10))
        assert np.linalg.norm(M - other) > np.linalg.norm(M - best)


def test_rank_for():
    assert sub.rank_for(M, 0.01) == 3
    assert sub.rank_for(M, 0.0) == 8
