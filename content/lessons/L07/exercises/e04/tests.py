import numpy as np
import sub

rng = np.random.default_rng(4)
X = rng.normal(size=(8, 5))
y = rng.integers(0, 3, size=8)


def test_init_shapes_and_scale():
    p = sub.init_mlp([5, 7, 6, 3], seed=0)
    assert sorted(p) == ["W1", "W2", "W3", "b1", "b2", "b3"]
    assert p["W2"].shape == (7, 6) and np.all(p["b2"] == 0)
    big = sub.init_mlp([400, 400], seed=1)["W1"]
    assert abs(big.std() - np.sqrt(2 / 400)) < 0.005


def test_grad_every_parameter():
    for act in ["tanh", "relu"]:
        p = sub.init_mlp([5, 7, 6, 3], seed=2)
        loss, g = sub.loss_and_grads(p, X, y, act)
        for k in p:
            num = np.zeros_like(p[k])
            for idx in np.ndindex(p[k].shape):
                old = p[k][idx]
                p[k][idx] = old + 1e-6
                lp, _ = sub.loss_and_grads(p, X, y, act)
                p[k][idx] = old - 1e-6
                lm, _ = sub.loss_and_grads(p, X, y, act)
                p[k][idx] = old
                num[idx] = (lp - lm) / 2e-6
            rel = np.linalg.norm(g[k] - num) / (np.linalg.norm(g[k]) + np.linalg.norm(num) + 1e-12)
            assert rel < 1e-5, (act, k, rel)


def test_predict_shape():
    p = sub.init_mlp([5, 4, 3])
    assert sub.predict(p, X).shape == (8,)
