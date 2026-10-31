import numpy as np
import sub


def test_grad_log_partition():
    t = np.array([0.5, -1.0, 2.0, 0.0])
    h = 1e-6
    num = np.array([(sub.log_partition(t + h * e) - sub.log_partition(t - h * e)) / (2 * h) for e in np.eye(4)])
    assert np.allclose(num, sub.grad_log_partition(t), atol=1e-9)
    p = sub.grad_log_partition(t)
    H = np.array([(sub.grad_log_partition(t + h * e) - sub.grad_log_partition(t - h * e)) / (2 * h) for e in np.eye(4)])
    assert np.allclose(H, np.diag(p) - np.outer(p, p), atol=1e-8)
    assert np.linalg.eigvalsh(H).min() > -1e-9


def test_fit_reaches_the_frequencies():
    c = np.array([30.0, 10.0, 50.0, 10.0])
    th = sub.fit(c)
    assert np.allclose(sub.grad_log_partition(th), c / c.sum(), atol=1e-4)
    assert sub.nll(th, c) <= sub.nll(np.log(c / c.sum()), c) + 1e-3
