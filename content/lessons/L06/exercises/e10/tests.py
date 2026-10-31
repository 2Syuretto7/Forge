import numpy as np
import sub

rng = np.random.default_rng(10)
x = rng.normal(size=8)
A = rng.normal(size=(15, 8))
B = rng.normal(size=(15, 8)) * 3 + 1


def test_batch_norm_depends_on_the_batch():
    assert sub.batch_dependence("batch", x, A, B) > 0.3


def test_layer_norm_does_not():
    assert sub.batch_dependence("layer", x, A, B) < 1e-12


def test_noise_scales_like_inverse_sqrt():
    n = [sub.batch_mean_noise(b) for b in (1, 4, 16, 64)]
    for b, v in zip((1, 4, 16, 64), n):
        assert abs(v * np.sqrt(b) - 1) < 0.06, (b, v)
