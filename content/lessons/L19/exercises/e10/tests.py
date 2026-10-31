import numpy as np
import sub

rng = np.random.default_rng(0)
W = rng.normal(size=(5, 6)) * 0.3
v = rng.normal(size=5)
a1 = rng.normal(size=6)


def test_grad_metric():
    _, g = sub.metric_and_grad(a1, W, v)
    num = [(sub.metric_and_grad(a1 + e, W, v)[0] - sub.metric_and_grad(a1 - e, W, v)[0]) / 2e-6 for e in np.eye(6) * 1e-6]
    assert np.allclose(g, num, atol=1e-9)


def test_estimate_close_for_small_differences():
    a0 = a1 + 0.1 * rng.normal(size=6)
    est, exact = sub.attribution_patching(a1, a0, W, v), sub.exact_patching(a1, a0, W, v)
    assert np.allclose(est, exact, atol=2e-3)
    far = a1 + 3 * rng.normal(size=6)
    assert np.abs(sub.attribution_patching(a1, far, W, v) - sub.exact_patching(a1, far, W, v)).max() > 0.05
