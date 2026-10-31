import numpy as np
import sub

rng = np.random.default_rng(2)
Q, _ = np.linalg.qr(rng.normal(size=(6, 6)))
LAM = np.array([1.0, 2.0, 5.0, 10.0, 30.0, 50.0])
A = Q @ np.diag(LAM) @ Q.T


def _run(lr, steps, x0):
    x = x0.copy()
    norms = [np.linalg.norm(x)]
    for _ in range(steps):
        x = x - lr * (A @ x)
        norms.append(np.linalg.norm(x))
    return np.array(norms)


def test_rates_diag():
    r = sub.rates(np.diag([1.0, 100.0]))
    assert abs(r["kappa"] - 100) < 1e-9 and abs(r["lr_max"] - 0.02) < 1e-12
    assert abs(r["lr_opt"] - 2 / 101) < 1e-12 and abs(r["rho_opt"] - 99 / 101) < 1e-12


def test_rotation_invariant():
    r = sub.rates(A)
    assert abs(r["kappa"] - 50) < 1e-8 and abs(r["lr_max"] - 0.04) < 1e-10


def test_contraction_matches_iteration():
    lr = 0.7 * sub.rates(A)["lr_max"]
    norms = _run(lr, 400, rng.normal(size=6))
    assert abs(norms[-1] / norms[-2] - sub.contraction(A, lr)) < 1e-3


def test_divergence_threshold():
    x0 = rng.normal(size=6)
    lr_max = sub.rates(A)["lr_max"]
    assert _run(1.02 * lr_max, 600, x0)[-1] > 10 * np.linalg.norm(x0)
    assert _run(0.98 * lr_max, 600, x0)[-1] < np.linalg.norm(x0)


def test_steps_needed():
    D = np.diag([1.0, 100.0])
    assert sub.steps_needed(D, 1e-6) == 691
    t = sub.steps_needed(A, 1e-4)
    norms = _run(sub.rates(A)["lr_opt"], t, rng.normal(size=6))
    assert norms[-1] <= 1e-4 * norms[0]
