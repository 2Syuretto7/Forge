import numpy as np
import sub

E, A, B, al, be = 1.69, 406.4, 410.7, 0.34, 0.28


def law(N, D):
    return E + A * N ** -al + B * D ** -be


def test_vertex_of_an_exact_parabola():
    N = np.exp(np.linspace(10, 20, 7))
    L = 3 + 0.02 * (np.log(N) - 14.5) ** 2
    n, l = sub.isoflop_minimum(N, L)
    assert abs(np.log(n) - 14.5) < 1e-9 and abs(l - 3) < 1e-9


def test_recovers_the_allocation_exponent():
    C = np.logspace(18, 21, 7)
    best = []
    for c in C:
        guess = (c / 6) ** 0.45
        N = guess * np.logspace(-1, 1, 9)
        best.append(sub.isoflop_minimum(N, law(N, c / (6 * N)))[0])
    assert abs(sub.allocation_exponent(C, np.array(best)) - be / (al + be)) < 0.01
