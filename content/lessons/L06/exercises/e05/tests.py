import numpy as np
import sub


def test_prediction():
    assert abs(sub.predicted_growth(20, 1.0) - 1024) < 1e-9
    assert abs(sub.predicted_growth(1000, 1 / np.sqrt(1000)) - np.sqrt(np.e)) < 1e-3


def test_linear_branch_follows_prediction():
    for alpha in (1.0, 0.5, 1 / np.sqrt(20)):
        r = sub.residual_rms(20, alpha)
        assert len(r) == 21
        assert abs(np.log(r[-1] / r[0]) - np.log(sub.predicted_growth(20, alpha))) < 0.1, alpha


def test_relu_branch_grows_faster():
    r = sub.residual_rms(20, 1.0, branch="relu")
    assert r[-1] / r[0] > 5 * sub.predicted_growth(20, 1.0)


def test_scaled_branches_stay_bounded():
    r = sub.residual_rms(60, 1 / np.sqrt(60))
    assert r[-1] / r[0] < 2.0
