import numpy as np
import sub


def test_ema_debias():
    assert np.allclose(sub.ema([3.0] * 10, 0.9, debias=True), 3.0)
    raw = sub.ema([3.0] * 10, 0.9)
    assert abs(raw[0] - 0.3) < 1e-12 and abs(raw[9] - 3 * (1 - 0.9 ** 10)) < 1e-12


def test_gains():
    assert abs(sub.momentum_gain(0.9, 0.0) - 10) < 1e-9
    assert abs(sub.momentum_gain(0.9, np.pi) - 1 / 1.9) < 1e-9
    assert abs(sub.ema_gain(0.9, 0.0) - 1) < 1e-9


def test_gain_matches_simulation():
    t = np.arange(1, 601)
    for omega in [np.pi / 6, np.pi / 2, 2 * np.pi / 3]:
        g = np.cos(omega * t)
        out = sub.ema(g, 0.8)
        tail = slice(400, 600)
        basis = np.column_stack([np.cos(omega * t[tail]), np.sin(omega * t[tail])])
        coef, *_ = np.linalg.lstsq(basis, out[tail], rcond=None)
        amp = np.hypot(*coef)
        assert abs(amp - sub.ema_gain(0.8, omega)) < 1e-3 * amp, omega


def test_low_pass():
    gains = [sub.momentum_gain(0.95, w) for w in np.linspace(0, np.pi, 9)]
    assert all(a > b for a, b in zip(gains, gains[1:]))
