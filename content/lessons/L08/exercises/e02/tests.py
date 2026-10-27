import numpy as np
import sub

rng = np.random.default_rng(2)


def test_bias():
    G = rng.normal(size=(32, 4))
    out = sub.unbroadcast(G, (4,))
    assert out.shape == (4,)
    assert np.allclose(out, G.sum(axis=0))


def test_column():
    G = rng.normal(size=(32, 4))
    out = sub.unbroadcast(G, (32, 1))
    assert out.shape == (32, 1)
    assert np.allclose(out, G.sum(axis=1, keepdims=True))


def test_scalar_and_identity():
    G = rng.normal(size=(2, 3, 5))
    assert np.shape(sub.unbroadcast(G, ())) == ()
    assert np.isclose(sub.unbroadcast(G, ()), G.sum())
    assert np.allclose(sub.unbroadcast(G, (2, 3, 5)), G)


def test_mixed():
    G = rng.normal(size=(6, 2, 3, 5))
    out = sub.unbroadcast(G, (2, 1, 5))
    assert out.shape == (2, 1, 5)
    assert np.allclose(out, G.sum(axis=(0, 2))[:, None, :])


def test_grad_matches_finite_differences():
    for shape in [(4,), (3, 1), (1, 4), (), (1,)]:
        Z = rng.normal(size=(3, 4))
        G = rng.normal(size=(3, 4))
        x = rng.normal(size=shape)
        f = lambda x: np.sum(G * (Z + x))
        num = np.zeros_like(x)
        for idx in np.ndindex(x.shape):
            e = np.zeros_like(x)
            e[idx] = 1e-6
            num[idx] = (f(x + e) - f(x - e)) / 2e-6
        assert np.allclose(sub.unbroadcast(G, x.shape), num, atol=1e-6), shape
