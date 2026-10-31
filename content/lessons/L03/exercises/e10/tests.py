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


X, y = _spiral()


def test_symmetric_units_never_separate():
    p = sub.symmetric_init([2, 8, 3], 0.1)
    assert sub.unit_spread(p["W1"]) == 0.0
    sub.train_full_batch(p, X, y, lr=0.5, steps=1500)
    assert sub.unit_spread(p["W1"]) < 1e-12, "all hidden units must stay identical"


def test_random_init_does_much_better():
    sym = sub.symmetric_init([2, 8, 3], 0.1)
    loss_sym = sub.train_full_batch(sym, X, y, lr=0.5, steps=1500)
    rng = np.random.default_rng(0)
    rnd = {"W1": rng.normal(size=(2, 8)), "b1": np.zeros(8), "W2": rng.normal(size=(8, 3)) * 0.5, "b2": np.zeros(3)}
    loss_rnd = sub.train_full_batch(rnd, X, y, lr=0.5, steps=1500)
    assert loss_rnd < 0.8 * loss_sym, (loss_rnd, loss_sym)
