import numpy as np
import sub

rng = np.random.default_rng(10)
X = rng.normal(size=(30, 4))
Y = X @ np.array([0.5, -0.5, 1.0, 0.0]) + rng.normal(size=30)


def test_map_minimizes_the_posterior():
    w = sub.map_estimate(X, Y, 1.0, 0.5)
    assert np.allclose(w, sub.ridge(X, Y, 4.0))
    best = sub.neg_log_posterior(w, X, Y, 1.0, 0.5)
    for _ in range(20):
        assert sub.neg_log_posterior(w + 0.01 * rng.normal(size=4), X, Y, 1.0, 0.5) > best


def test_limits():
    ls = np.linalg.lstsq(X, Y, rcond=None)[0]
    assert np.allclose(sub.map_estimate(X, Y, 1.0, 1e4), ls, atol=1e-6)
    norms = [np.linalg.norm(sub.map_estimate(X, Y, 1.0, t)) for t in (10.0, 1.0, 0.1, 0.01)]
    assert all(a > b for a, b in zip(norms, norms[1:])) and norms[-1] < 0.05


def test_prior_helps_with_little_data():
    wins = 0
    for s in range(40):
        r = np.random.default_rng(100 + s)
        w_true = r.normal(0, 0.5, size=8)
        Xs, Xt = r.normal(size=(10, 8)), r.normal(size=(500, 8))
        ys, yt = Xs @ w_true + r.normal(size=10), Xt @ w_true + r.normal(size=500)
        e_ls = np.mean((yt - Xt @ np.linalg.lstsq(Xs, ys, rcond=None)[0]) ** 2)
        e_map = np.mean((yt - Xt @ sub.map_estimate(Xs, ys, 1.0, 0.5)) ** 2)
        wins += e_map < e_ls
    assert wins >= 32, wins
