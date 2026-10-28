import numpy as np
import sub


def test_small_cases():
    req = [(0, 3), (0, 1), (1, 2)]
    assert sub.static_batching(req, 2) == [3, 1, 5]
    assert sub.continuous_batching(req, 2) == [3, 1, 3]


def test_continuous_is_faster():
    rng = np.random.default_rng(0)
    arr = np.sort(rng.integers(0, 40, 30))
    req = list(zip(arr.tolist(), rng.integers(2, 40, 30).tolist()))
    lat_s = np.mean(np.array(sub.static_batching(req, 8)) - arr)
    lat_c = np.mean(np.array(sub.continuous_batching(req, 8)) - arr)
    assert lat_c < 0.6 * lat_s
    assert all(f >= a + n for f, (a, n) in zip(sub.continuous_batching(req, 8), req))
