import numpy as np
import sub

P = dict(E=1.69, A=406.4, B=410.7, alpha=0.34, beta=0.28)


def optimal(C):
    a, b = P["alpha"], P["beta"]
    G = (a * P["A"] / (b * P["B"])) ** (1 / (a + b))
    N = G * (C / 6) ** (b / (a + b))
    return N, C / (6 * N)


def test_tokens_needed():
    N = 1e9
    D = sub.tokens_needed(N, 2.2, **P)
    assert abs(sub.law(N, D, **P) - 2.2) < 1e-9
    assert sub.tokens_needed(1e6, 2.0, **P) == np.inf


def test_no_inference_is_compute_optimal():
    N0, D0 = optimal(1e22)
    target = sub.law(N0, D0, **P)
    N, D, cost = sub.cheapest_model(target, 0.0, **P)
    assert abs(np.log(N / N0)) < 0.01 and abs(cost / 1e22 - 1) < 1e-3


def test_inference_favours_smaller_models_on_more_tokens():
    N0, D0 = optimal(1e22)
    target = sub.law(N0, D0, **P)
    N, D, cost = sub.cheapest_model(target, 1e13, **P)
    assert N < 0.5 * N0 and D / N > 3 * D0 / N0
    assert cost < 6 * N0 * D0 + 2 * N0 * 1e13
