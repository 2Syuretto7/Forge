import numpy as np
import sub


def test_dyadic_distribution_is_coded_exactly():
    p = np.array([0.5, 0.25, 0.125, 0.125])
    L = sub.shannon_lengths(p)
    assert list(L) == [1, 2, 3, 3]
    assert sub.kraft_sum(L) == 1.0
    assert abs(sub.expected_length(p, L) - sub.entropy_bits(p)) < 1e-12


def test_bounds_on_random_distributions():
    rng = np.random.default_rng(13)
    for _ in range(200):
        p = rng.dirichlet(np.ones(rng.integers(2, 20)))
        L = sub.shannon_lengths(p)
        assert sub.kraft_sum(L) <= 1 + 1e-12
        H = sub.entropy_bits(p)
        assert H - 1e-12 <= sub.expected_length(p, L) < H + 1
