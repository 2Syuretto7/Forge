import numpy as np
import sub


def test_simple_hinges():
    assert sub.count_pieces(np.array([1.0]), np.array([0.0]), np.array([1.0])) == 2
    assert sub.count_pieces(np.array([1.0, 1.0]), np.array([0.0, -1.0]), np.array([1.0, -2.0])) == 3


def test_at_most_k_plus_one_pieces():
    rng = np.random.default_rng(9)
    for k in [3, 6, 10]:
        for _ in range(5):
            kinks = np.sort(rng.uniform(-2.5, 2.5, size=k))
            if np.min(np.diff(kinks)) < 0.05:
                continue
            w = rng.choice([-1.0, 1.0], size=k) * rng.uniform(0.5, 2, size=k)
            b = -w * kinks
            a = rng.choice([-1.0, 1.0], size=k) * rng.uniform(0.5, 2, size=k)
            assert np.allclose(sub.kink_locations(w, b), kinks)
            assert sub.count_pieces(w, b, a) == k + 1
