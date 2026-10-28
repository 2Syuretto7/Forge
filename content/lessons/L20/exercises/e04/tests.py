import numpy as np
import sub

rng = np.random.default_rng(2)


def test_merge():
    x, W0, A, B = rng.normal(size=(3, 6)), rng.normal(size=(4, 6)), rng.normal(size=(2, 6)), rng.normal(size=(4, 2))
    y = x @ W0.T + 8.0 / 2 * (x @ A.T) @ B.T
    assert np.allclose(x @ sub.merge(W0, A, B, 8.0).T, y)


def test_counts():
    assert sub.lora_params(4096, 4096, 8) == 65536
    f = sub.trainable_fraction(32, 4096, 8)
    assert abs(f - 2 * 65536 / (12 * 4096 ** 2)) < 1e-15 and f < 0.001
    assert sub.trainable_fraction(1, 4096, 8) == f
