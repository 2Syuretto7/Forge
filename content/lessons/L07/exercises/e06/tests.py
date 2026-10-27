import numpy as np
import sub


def _spiral(n=100, K=3, seed=0):
    rng = np.random.default_rng(seed)
    Xs, ys = [], []
    for j in range(K):
        r = np.linspace(0.0, 1.0, n)
        t = np.linspace(4 * j, 4 * (j + 1), n) + 0.2 * rng.normal(size=n)
        Xs.append(np.column_stack([r * np.sin(t), r * np.cos(t)]))
        ys.append(np.full(n, j))
    return np.concatenate(Xs), np.concatenate(ys)


def test_sgd_step():
    p = {"W1": np.ones((2, 2)), "b1": np.zeros(2)}
    sub.sgd_step(p, {"W1": np.ones((2, 2)), "b1": np.ones(2)}, 0.5)
    assert np.allclose(p["W1"], 0.5) and np.allclose(p["b1"], -0.5)


def test_mlp_learns_the_spiral():
    X, y = _spiral()
    p = sub.init_mlp([2, 100, 3], seed=0)
    losses = sub.train(p, X, y, lr=1.0, epochs=150, batch=32, seed=0)
    assert len(losses) == 150 * 10
    assert np.mean(losses[-10:]) < 0.3 * np.mean(losses[:10])
    assert np.mean(sub.predict(p, X) == y) > 0.95
