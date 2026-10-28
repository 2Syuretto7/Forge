import numpy as np
import sub

rng = np.random.default_rng(11)
x = rng.normal(size=6) * 4
gamma = rng.normal(size=6) + 1
beta = rng.normal(size=6)


def test_batch_norm_outputs_beta():
    y, dx = sub.batch_of_one(x, gamma, beta)
    assert np.allclose(y, beta)
    y2, _ = sub.batch_of_one(x * 10 - 3, gamma, beta)
    assert np.allclose(y2, beta)


def test_batch_norm_passes_no_gradient():
    _, dx = sub.batch_of_one(x, gamma, beta)
    assert np.allclose(dx, 0)


def test_layer_norm_still_works():
    y, dx = sub.layernorm_of_one(x, gamma, beta)
    assert not np.allclose(y, beta)
    assert np.abs(dx).max() > 0.01
