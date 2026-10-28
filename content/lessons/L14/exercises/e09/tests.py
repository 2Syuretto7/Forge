import numpy as np
import sub

rng = np.random.default_rng(9)
Z = rng.normal(size=(4, 7)) * 2
Y = rng.integers(0, 7, size=4)


def test_grad_tempered():
    for T in (0.5, 2.0):
        _, g = sub.tempered_xent(Z, Y, T)
        num = np.zeros_like(Z)
        for idx in np.ndindex(Z.shape):
            E = np.zeros_like(Z)
            E[idx] = 1e-6
            num[idx] = (sub.tempered_xent(Z + E, Y, T)[0] - sub.tempered_xent(Z - E, Y, T)[0]) / 2e-6
        assert np.allclose(g, num, atol=1e-8), T


def test_entropy_increases():
    z = np.array([3.0, 1.0, 0.5, 0.0, -2.0])
    e = [sub.entropy_at(z, T) for T in (0.01, 0.5, 1.0, 2.0, 100.0)]
    assert e[0] < 1e-6 and all(a < b for a, b in zip(e, e[1:])) and abs(e[-1] - np.log(5)) < 1e-3
