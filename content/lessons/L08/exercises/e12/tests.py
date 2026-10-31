import numpy as np
import sub

rng = np.random.default_rng(12)
X = rng.normal(size=(3, 100))


def test_masked_is_correct():
    assert np.allclose(sub.blocked_row_sums(X, 64), X.sum(axis=1))
    assert np.allclose(sub.blocked_row_sums(X, 128), X.sum(axis=1))


def test_unmasked_reads_neighbours():
    bad = sub.blocked_row_sums(X, 64, masked=False)
    assert np.isclose(bad[0], X[0].sum() + X[1, :28].sum())
    assert np.isclose(bad[2], X[2].sum() + 28 * 1000.0)


def test_programs():
    assert sub.programs_needed(100, 64) == 2 and sub.programs_needed(128, 64) == 2 and sub.programs_needed(129, 64) == 3
