import numpy as np
import sub

X = np.logspace(0, 2, 30)


def test_bootstrap_agrees_with_jacobian():
    rng = np.random.default_rng(1)
    y = sub.model([1.7, 2.0, 0.5], X) + 0.01 * rng.standard_normal(30)
    th = sub.fit(X, y, [1.5, 1.5, 0.4])
    boots = sub.residual_bootstrap(X, y, th, 300, rng)
    assert boots.shape == (300, 3)
    r = y - sub.model(th, X)
    J = sub.jacobian(th, X)
    se = np.sqrt(np.diag((r @ r) / 27 * np.linalg.inv(J.T @ J)))
    assert abs(boots[:, 2].std() / se[2] - 1) < 0.3, (boots[:, 2].std(), se[2])
    lo, hi = sub.percentile_interval(boots)
    assert lo[2] < 0.5 < hi[2] and lo[0] < 1.7 < hi[0]
