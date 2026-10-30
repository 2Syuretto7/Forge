import numpy as np
import sub


def f(Ws, w, x):
    h = x
    for W in Ws:
        h = np.tanh(W @ h)
    return w @ h


def test_grad_both_modes_agree():
    Ws, w = sub.make_net(10)
    x = np.random.default_rng(2).normal(size=10)
    a, b = sub.forward_mode_grad(Ws, w, x), sub.reverse_mode_grad(Ws, w, x)
    assert np.allclose(a, b, atol=1e-12)
    num = np.array([(f(Ws, w, x + 1e-6 * e) - f(Ws, w, x - 1e-6 * e)) / 2e-6 for e in np.eye(10)])
    assert np.allclose(b, num, atol=1e-8)


def test_reverse_wins_for_many_inputs():
    assert sub.time_ratio(400) > 3
