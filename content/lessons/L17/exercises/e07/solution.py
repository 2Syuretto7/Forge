import numpy as np


def bt_loss(w, F_win, F_lose):
    """A linear reward r = F w. The Bradley-Terry negative log-likelihood that the preferred
    response wins, mean over pairs of log(1 + exp(-(r_win - r_lose))), and its gradient."""
    d = (F_win - F_lose) @ w
    loss = np.mean(np.logaddexp(0, -d))
    s = 1 / (1 + np.exp(d))  # sigmoid(-d)
    return float(loss), -(F_win - F_lose).T @ s / len(d)


def fit_bt(F_win, F_lose, steps=2000, lr=1.0):
    """Gradient descent from zero."""
    w = np.zeros(F_win.shape[1])
    for _ in range(steps):
        _, g = bt_loss(w, F_win, F_lose)
        w -= lr * g
    return w
