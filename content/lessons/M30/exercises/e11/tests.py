import numpy as np
import sub

R = sub.make_rewards()
TAUS = np.geomspace(1e-3, 1e3, 13)


def test_sweep():
    H, ER = sub.sweep(R, TAUS)
    assert np.all(np.isfinite(H)) and np.all(np.isfinite(ER))
    assert np.all(np.diff(H) > -1e-9) and np.all(np.diff(ER) < 1e-9)
    assert np.exp(H[0]) < 5 and np.exp(H[-1]) > 0.99e6
    assert abs(ER[0] - R.max()) < 0.05 and abs(ER[-1] - R.mean()) < 0.01


def test_entropy_helpers():
    p = np.full(4, 0.25)
    assert abs(sub.entropy(p) - np.log(4)) < 1e-12 and abs(sub.effective_actions(p) - 4) < 1e-9
    assert sub.entropy([1.0, 0.0]) == 0.0
