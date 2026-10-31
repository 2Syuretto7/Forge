import numpy as np
import sub

rng = np.random.default_rng(8)
true_w = np.array([1.5, -1.0, 0.5])
F = rng.normal(size=(400, 3))
i, j = rng.integers(0, 400, 600), rng.integers(0, 400, 600)
p_win = 1 / (1 + np.exp(-(F[i] - F[j]) @ true_w))
first = rng.random(600) < p_win
F_win = np.where(first[:, None], F[i], F[j])
F_lose = np.where(first[:, None], F[j], F[i])


def test_grad_bt():
    w = np.array([0.3, 0.2, -0.1])
    _, g = sub.bt_loss(w, F_win, F_lose)
    num = [(sub.bt_loss(w + e, F_win, F_lose)[0] - sub.bt_loss(w - e, F_win, F_lose)[0]) / 2e-6 for e in np.eye(3) * 1e-6]
    assert np.allclose(g, num, atol=1e-8)


def test_recovers_the_reward():
    w = sub.fit_bt(F_win, F_lose)
    assert np.corrcoef(F @ w, F @ true_w)[0, 1] > 0.98
