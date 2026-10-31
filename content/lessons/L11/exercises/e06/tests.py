import numpy as np
import sub

P = dict(E=1.69, A=406.4, B=410.7, alpha=0.34, beta=0.28)


def test_grad_dloss_dlogN():
    C = 1e21
    for N in [1e8, 1e9, 1e10]:
        h = 1e-5
        up = sub.law(N * np.exp(h), C / (6 * N * np.exp(h)), **P)
        down = sub.law(N * np.exp(-h), C / (6 * N * np.exp(-h)), **P)
        assert abs(sub.dloss_dlogN(N, C, **P) - (up - down) / (2 * h)) < 1e-8


def test_optimum_beats_every_other_split():
    for C in [1e19, 1e22]:
        N, D, loss = sub.optimal_allocation(C, **P)
        assert abs(6 * N * D / C - 1) < 1e-12
        assert abs(sub.dloss_dlogN(N, C, **P)) < 1e-10
        sizes = N * np.logspace(-1, 1, 41)
        assert loss <= sub.law(sizes, C / (6 * sizes), **P).min() + 1e-12


def test_more_compute_more_of_both():
    N1, D1, L1 = sub.optimal_allocation(1e20, **P)
    N2, D2, L2 = sub.optimal_allocation(1e21, **P)
    assert abs(N2 / N1 - 10 ** (0.28 / 0.62)) < 1e-9 and abs(D2 / D1 - 10 ** (0.34 / 0.62)) < 1e-9
    assert L2 < L1
