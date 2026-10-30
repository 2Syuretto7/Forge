import numpy as np
import sub

rng = np.random.default_rng(7)
Qm, _ = np.linalg.qr(rng.normal(size=(6, 6)))
S = Qm @ np.diag([10.0, 9.0, 1.0, 0.5, 0.2, 0.1]) @ Qm.T
v1 = Qm[:, 0] * np.sign(Qm[np.argmax(np.abs(Qm[:, 0])), 0])


def test_top_eigenpair():
    lam, v = sub.power_iteration(S, 400, seed=0)
    assert abs(lam - 10.0) < 1e-8
    assert np.allclose(v, v1, atol=1e-6)
    assert v[np.argmax(np.abs(v))] > 0


def test_rate_matches_theory():
    def tan_err(v):
        c = abs(v @ v1)
        return np.sqrt(max(1 - c * c, 0)) / c
    _, a = sub.power_iteration(S, 20, seed=0)
    _, b = sub.power_iteration(S, 40, seed=0)
    ratio = tan_err(b) / tan_err(a)
    assert 0.6 * 0.9 ** 20 < ratio < 1.6 * 0.9 ** 20


def test_gap_and_count():
    assert abs(sub.gap_ratio(S) - 0.9) < 1e-12
    assert sub.iterations_needed(0.9, 1e-6) == 132
    assert sub.iterations_needed(0.5, 0.25) == 2
    assert isinstance(sub.iterations_needed(0.5, 0.1), int)
