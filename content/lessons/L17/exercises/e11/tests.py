import warnings
import numpy as np
import sub

rng = np.random.default_rng(11)
Q = rng.normal(size=(8, 64)) * 80
K = rng.normal(size=(8, 64)) * 80


def test_fp16_scores_overflow():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s = sub.scores(Q, K, np.float16)
    assert s.dtype == np.float16 and not np.all(np.isfinite(s))
    assert np.all(np.isfinite(sub.scaled_first(Q, K, np.float16)))


def test_grad_stable_lse():
    x = np.array([1000.0, 999.0, 1001.5, 990.0])
    v, g = sub.stable_lse(x)
    assert np.isfinite(v) and np.isclose(g.sum(), 1.0)
    num = np.array([(sub.stable_lse(x + e)[0] - sub.stable_lse(x - e)[0]) / 2e-6 for e in np.eye(4) * 1e-6])
    assert np.allclose(g, num, atol=1e-6)
