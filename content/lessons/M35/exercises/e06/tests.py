import numpy as np
import sub

X = np.logspace(0, 2, 30)
TRUE = np.array([1.7, 2.0, 0.5])


def test_se_matches_spread():
    rng = np.random.default_rng(0)
    fits, ses = [], []
    for _ in range(300):
        y = sub.model(TRUE, X) + 0.01 * rng.standard_normal(30)
        th = sub.fit(X, y, [1.5, 1.5, 0.4])
        fits.append(th)
        ses.append(sub.standard_errors(X, y, th))
    spread = np.std(np.array(fits)[:, 2])
    typical = np.median(np.array(ses)[:, 2])
    assert abs(typical / spread - 1) < 0.2, (typical, spread)
