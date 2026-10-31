import numpy as np
import sub

X = np.logspace(0, 2, 30)


def test_lm_rescues_bad_starts():
    rng = np.random.default_rng(0)
    y = sub.model([1.7, 2.0, 0.5], X) + 0.003 * rng.standard_normal(30)
    best, _ = sub.levenberg_marquardt(X, y, [1.5, 1.5, 0.4])
    best_loss = sub.sse(best, X, y)
    for start in ([0.0, 0.1, 0.05], [1.0, 5.0, 3.0]):
        th, hist = sub.levenberg_marquardt(X, y, start)
        assert abs(sub.sse(th, X, y) - best_loss) < 1e-9 and np.max(np.abs(th - best)) < 1e-4
        assert all(b <= a for a, b in zip(hist, hist[1:]))
        assert sub.sse(sub.gauss_newton(X, y, start), X, y) > 100 * best_loss
