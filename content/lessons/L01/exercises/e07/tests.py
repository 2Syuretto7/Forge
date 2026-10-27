import numpy as np
import sub

rng = np.random.default_rng(7)
Qm, _ = np.linalg.qr(rng.normal(size=(6, 6)))
eigs = np.array([10.0, 9.0, 1.0, 0.5, 0.2, 0.1])
S = Qm @ np.diag(eigs) @ Qm.T
v1 = Qm[:, 0] * np.sign(Qm[np.argmax(np.abs(Qm[:, 0])), 0])


def test_finds_top_eigenpair():
    lam, v = sub.power_iteration(S, 400, seed=0)
    assert abs(lam - 10.0) < 1e-8, f"lambda = {lam}"
    assert np.allclose(v, v1, atol=1e-6)
    assert abs(np.linalg.norm(v) - 1) < 1e-12


def test_sign_convention():
    _, v = sub.power_iteration(S, 400, seed=3)
    assert v[np.argmax(np.abs(v))] > 0


def test_convergence_rate_matches_theory():
    def tan_err(v):
        c = abs(v @ v1)
        return np.sqrt(max(1 - c * c, 0)) / c
    _, a = sub.power_iteration(S, 20, seed=0)
    _, b = sub.power_iteration(S, 40, seed=0)
    ratio = tan_err(b) / tan_err(a)
    expected = 0.9 ** 20
    assert 0.6 * expected < ratio < 1.6 * expected, f"error shrank by {ratio:.4f}, theory says {expected:.4f}"


def test_gap_ratio_and_iteration_count():
    assert abs(sub.gap_ratio(S) - 0.9) < 1e-12
    assert sub.iterations_needed(0.9, 1e-6) == 132
    assert sub.iterations_needed(0.5, 0.25) == 2
    assert isinstance(sub.iterations_needed(0.5, 0.1), int)
