import numpy as np
import sub

rng = np.random.default_rng(9)


def _calibrated(n):
    p1 = rng.uniform(0.5, 1.0, size=n)
    y = (rng.uniform(size=n) >= p1).astype(int)  # class 0 with probability p1
    P = np.column_stack([p1, 1 - p1])
    return P, y


def test_bins_basic():
    P = np.array([[0.95, 0.05], [0.55, 0.45], [0.65, 0.35], [1.0, 0.0]])
    y = np.array([0, 1, 0, 0])
    conf, acc, cnt = sub.calibration_bins(P, y, 10)
    assert cnt[9] == 2 and cnt[5] == 1 and cnt[6] == 1
    assert abs(conf[9] - 0.975) < 1e-12 and acc[9] == 1.0 and acc[5] == 0.0


def test_calibrated_predictor_has_small_ece():
    P, y = _calibrated(40000)
    assert sub.ece(P, y, 10) < 0.01


def test_overconfident_predictor():
    P, y = _calibrated(40000)
    sharp = P ** 3
    sharp /= sharp.sum(axis=1, keepdims=True)
    assert sub.ece(sharp, y, 10) > 0.05
    conf, acc, cnt = sub.calibration_bins(sharp, y, 10)
    m = cnt > 100
    assert np.all(conf[m] >= acc[m] - 0.02), "overconfident: confidence above accuracy"
