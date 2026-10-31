import numpy as np
import sub

L = np.array([2.0, 1.0, 0.0, -1.0])


def test_temperature():
    assert np.isclose(sub.softmax_t(np.array([2.0, 1.0, 0.0]))[0], 0.6652, atol=1e-4)
    assert np.isclose(sub.softmax_t(np.array([2.0, 1.0, 0.0]), 0.5)[0], 0.8668, atol=1e-4)
    assert sub.softmax_t(L, 1e-3)[0] > 0.999


def test_filters():
    k = sub.top_k_filter(L, 2)
    assert np.isfinite(k).tolist() == [True, True, False, False]
    probs = sub.softmax_t(L)
    p = sub.top_p_filter(L, 0.9)
    kept = np.isfinite(p).sum()
    assert probs[:kept - 1].sum() < 0.9 <= probs[:kept].sum()
    assert np.isfinite(sub.top_p_filter(L, 0.5)).sum() == 1


def test_sample():
    rng = np.random.default_rng(0)
    draws = [sub.sample(L, rng, T=1.0, k=2) for _ in range(300)]
    assert set(draws) <= {0, 1} and 0.6 < np.mean(np.array(draws) == 0) < 0.85
    assert all(sub.sample(L, rng, T=1e-4) == 0 for _ in range(20))
