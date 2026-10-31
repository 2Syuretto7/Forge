import numpy as np


def mse_grad(w, X, y):
    """L = mean((X w - y)^2) / 2 and its gradient."""
    r = X @ w - y
    return 0.5 * float(np.mean(r * r)), X.T @ r / len(y)


def train(X, y, lr, steps, master):
    """Gradient descent where the forward and backward pass use float16 copies of w. With
    master=True, a float32 master copy receives the updates; with master=False, w itself lives in
    float16 and every update is rounded to float16. Return the final float32 loss."""
    w32 = np.zeros(X.shape[1], dtype=np.float32)
    w16 = w32.astype(np.float16)
    X16, y16 = X.astype(np.float16), y.astype(np.float16)
    for _ in range(steps):
        _, g = mse_grad(w16.astype(np.float32), X16.astype(np.float32), y16.astype(np.float32))
        if master:
            w32 = (w32 - np.float32(lr) * g.astype(np.float32)).astype(np.float32)
            w16 = w32.astype(np.float16)
        else:
            w16 = (w16 - (np.float32(lr) * g).astype(np.float16)).astype(np.float16)
    return mse_grad(w16.astype(np.float64), X, y)[0]
