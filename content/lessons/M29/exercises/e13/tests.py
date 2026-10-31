import numpy as np
import sub


def test_plateau_is_noise():
    const = sub.sgd_constant(0.5, 20, np.random.default_rng(1))
    decay = sub.sgd_decaying(0.5, 20, np.random.default_rng(1))
    g_const, g_decay = sub.gap_to_optimum(const), sub.gap_to_optimum(decay)
    assert g_const > 0.01, g_const
    assert g_decay < g_const / 4, (g_const, g_decay)
    assert abs(const[-1] - const[-5]) < 0.05


def test_halving_lowers_the_plateau():
    a = np.mean(sub.sgd_constant(0.5, 20, np.random.default_rng(2))[-10:])
    b = np.mean(sub.sgd_constant(0.25, 20, np.random.default_rng(3))[-10:])
    assert b < a
