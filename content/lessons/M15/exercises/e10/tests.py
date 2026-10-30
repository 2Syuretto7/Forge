import math
import numpy as np
import sub

hs = 10.0 ** -np.arange(1, 15.5, 0.25)


def test_grad_v_shape():
    err = sub.sweep(math.exp, math.exp, 1.0, hs, "forward")
    assert err.shape == hs.shape
    i = int(np.argmin(err))
    assert err[0] > 100 * err[i] and err[-1] > 100 * err[i]


def test_grad_forward_minimum_matches_theory():
    err = sub.sweep(math.exp, math.exp, 1.0, hs, "forward")
    h_meas = sub.best_step(hs, err)
    h_pred = sub.predicted_best_step(math.e, math.e, 2.2e-16, "forward")
    assert 1e-9 < h_pred < 1e-7
    assert h_pred / 30 < h_meas < h_pred * 30, (h_meas, h_pred)


def test_grad_central_minimum_matches_theory():
    err = sub.sweep(math.exp, math.exp, 1.0, hs, "central")
    h_meas = sub.best_step(hs, err)
    h_pred = sub.predicted_best_step(math.e, math.e, 2.2e-16, "central")
    assert 1e-6 < h_pred < 1e-4
    assert h_pred / 30 < h_meas < h_pred * 30, (h_meas, h_pred)
    assert err.min() < 1e-9
