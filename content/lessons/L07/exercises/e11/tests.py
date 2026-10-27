import numpy as np
import sub

rng = np.random.default_rng(11)
X = rng.uniform(-1, 1, size=(200, 2))
y = rng.integers(0, 3, size=200)
params = {"W1": rng.normal(size=(2, 20)), "b1": np.zeros(20), "W2": rng.normal(size=(20, 3)), "b2": np.zeros(3)}


def test_healthy_network_has_no_dead_units():
    assert sub.dead_fraction(params["W1"], params["b1"], X) == 0.0


def test_negative_bias_kills_units_and_their_gradients():
    p = {k: v.copy() for k, v in params.items()}
    p["b1"][:14] = -5.0
    frac = sub.dead_fraction(p["W1"], p["b1"], X)
    assert abs(frac - 14 / 20) < 1e-12
    dW1, db1 = sub.first_layer_grads(p, X, y)
    assert np.all(dW1[:, :14] == 0.0) and np.all(db1[:14] == 0.0)
    assert np.any(dW1[:, 14:] != 0.0)
