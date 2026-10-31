import numpy as np
import sub

rng = np.random.default_rng(8)


def test_param_count():
    for d in (8, 16, 64):
        p = sub.init_block(d)
        assert sum(v.size for v in p.values()) == sub.block_param_count(d)
    assert sub.block_param_count(768) == 12 * 768 * 768 + 10 * 768


def test_block_shapes_and_residual():
    p = sub.init_block(16, seed=1)
    X = rng.normal(size=(7, 16))
    Y = sub.block_forward(X, p, 4)
    assert Y.shape == X.shape
    zero = {k: (np.zeros_like(v) if k[0] in "Wb" else v) for k, v in p.items()}
    assert np.allclose(sub.block_forward(X, zero, 4), X)


def test_block_is_causal():
    p = sub.init_block(16, seed=2)
    p = {k: v * 20 if k.startswith("W") else v for k, v in p.items()}
    X = rng.normal(size=(7, 16))
    Y = sub.block_forward(X, p, 4)
    X2 = X.copy()
    X2[4:] += 1.0
    Y2 = sub.block_forward(X2, p, 4)
    assert np.allclose(Y[:4], Y2[:4]) and not np.allclose(Y[4:], Y2[4:])
