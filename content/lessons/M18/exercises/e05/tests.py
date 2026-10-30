import numpy as np
import sub

rng = np.random.default_rng(6)
Ws = [rng.normal(size=(6, 4)), rng.normal(size=(5, 6)), rng.normal(size=(2, 5))]


def numjac(f, x, h=1e-6):
    m = f(x).size
    J = np.zeros((m, x.size))
    for j in range(x.size):
        e = np.zeros_like(x)
        e[j] = h
        J[:, j] = (f(x + e) - f(x - e)) / (2 * h)
    return J


def test_grad_network():
    x = rng.normal(size=4)
    J = sub.network_jacobian(Ws, x)
    assert J.shape == (2, 4)
    assert np.allclose(J, numjac(lambda v: sub.forward(Ws, v)[-1], x), atol=1e-8)
    assert [j.shape for j in sub.layer_jacobians(Ws, x)] == [(6, 4), (5, 6), (2, 5)]
