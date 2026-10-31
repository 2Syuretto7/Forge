import numpy as np
import sub


def test_scale_invariance():
    s = np.array([1.0, 10.0])
    a1 = sub.run_adam(sub.quadratic_grad(s), [1.0, 1.0], 200, 0.05)
    a2 = sub.run_adam(sub.quadratic_grad(1000 * s), [1.0, 1.0], 200, 0.05)
    assert np.max(np.abs(a1 - a2)) < 1e-6
    g1 = sub.run_sgd(sub.quadratic_grad(s), [1.0, 1.0], 200, 0.05)
    g2 = sub.run_sgd(sub.quadratic_grad(1000 * s), [1.0, 1.0], 200, 0.05)
    assert np.all(np.abs(g1[-1]) < 1e-3)
    assert not np.all(np.isfinite(g2[-1])) or np.max(np.abs(g2[-1])) > 1e6
