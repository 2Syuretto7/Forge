import numpy as np
import sub

rng = np.random.default_rng(1)


def test_rows_sum_to_one_and_stable():
    S = rng.normal(size=(3, 4, 5)) * 50 + 1000
    P = sub.softmax_rows(S)
    assert P.shape == S.shape and np.allclose(P.sum(axis=-1), 1)
    assert np.all(np.isfinite(P))


def test_masked_entries():
    S = np.array([[0.0, -np.inf, np.log(3)]])
    assert np.allclose(sub.softmax_rows(S), [[0.25, 0.0, 0.75]])


def test_grad_softmax():
    S = rng.normal(size=(4, 6))
    G = rng.normal(size=(4, 6))
    P = sub.softmax_rows(S)
    dS = sub.softmax_backward(P, G)
    num = np.zeros_like(S)
    for idx in np.ndindex(S.shape):
        E = np.zeros_like(S)
        E[idx] = 1e-6
        num[idx] = (np.sum(sub.softmax_rows(S + E) * G) - np.sum(sub.softmax_rows(S - E) * G)) / 2e-6
    assert np.allclose(dS, num, atol=1e-8)
