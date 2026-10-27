import numpy as np
import sub


def test_estimators():
    assert sub.mle_p(0, 3) == 0.0
    assert abs(sub.smoothed_p(0, 3, 1.0) - 0.2) < 1e-12
    assert abs(sub.smoothed_p(3, 4, 0.5) - 3.5 / 5) < 1e-12


def test_zero_probability_means_infinite_loss():
    assert sub.heldout_logloss(0.0, 1, 10) == float("inf")
    assert sub.heldout_logloss(1.0, 9, 10) == float("inf")
    assert abs(sub.heldout_logloss(0.0, 0, 10)) < 1e-12
    assert abs(sub.heldout_logloss(0.5, 3, 10) - np.log(2)) < 1e-12


def test_mle_blows_up_with_three_flips():
    mle = sub.expected_logloss(sub.mle_p, 0.3, 3, 20, 500, seed=1)
    smooth = sub.expected_logloss(lambda k, n: sub.smoothed_p(k, n, 1.0), 0.3, 3, 20, 500, seed=1)
    assert mle == float("inf")
    assert np.isfinite(smooth) and smooth < 1.0


def test_with_plenty_of_data_both_are_fine():
    mle = sub.expected_logloss(sub.mle_p, 0.3, 500, 20, 300, seed=2)
    smooth = sub.expected_logloss(lambda k, n: sub.smoothed_p(k, n, 1.0), 0.3, 500, 20, 300, seed=2)
    assert np.isfinite(mle) and abs(mle - smooth) < 0.01
