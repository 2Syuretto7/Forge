import numpy as np
import sub

P = dict(E=1.69, A=406.4, B=410.7, alpha=0.34, beta=0.28)
NN, DD = np.meshgrid(np.logspace(7, 9, 5), np.logspace(8, 10, 5))
N, D = NN.ravel(), DD.ravel()
L = sub.law(N, D, **P)


def test_linear_solve_is_exact_at_the_true_exponents():
    E, A, B, sse = sub.fit_for_exponents(0.34, 0.28, N, D, L)
    assert abs(E - 1.69) < 1e-8 and abs(A / 406.4 - 1) < 1e-8 and abs(B / 410.7 - 1) < 1e-8 and sse < 1e-20


def test_recovers_noiseless_parameters():
    p = sub.fit_parametric(N, D, L)
    assert abs(p["alpha"] - 0.34) < 1e-6 and abs(p["beta"] - 0.28) < 1e-6 and abs(p["E"] - 1.69) < 1e-6


def test_predicts_a_larger_run_from_noisy_runs():
    rng = np.random.default_rng(0)
    p = sub.fit_parametric(N, D, L * (1 + 0.005 * rng.standard_normal(L.shape)))
    truth = sub.law(3e9, 3e10, **P)
    assert abs(sub.law(3e9, 3e10, **p) / truth - 1) < 0.015
