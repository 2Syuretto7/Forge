import numpy as np

GLYPHS = [
    ["..####..", ".##..##.", ".##..##.", ".##..##.", ".##..##.", ".##..##.", ".##..##.", "..####.."],
    ["...##...", "..###...", ".####...", "...##...", "...##...", "...##...", "...##...", ".######."],
    ["..####..", ".##..##.", ".....##.", "....##..", "...##...", "..##....", ".##.....", ".######."],
    ["..####..", ".##..##.", ".....##.", "...###..", ".....##.", ".....##.", ".##..##.", "..####.."],
    ["....##..", "...###..", "..####..", ".##.##..", ".######.", "....##..", "....##..", "....##.."],
    [".######.", ".##.....", ".##.....", ".#####..", ".....##.", ".....##.", ".##..##.", "..####.."],
    ["..####..", ".##.....", ".##.....", ".#####..", ".##..##.", ".##..##.", ".##..##.", "..####.."],
    [".######.", ".....##.", "....##..", "...##...", "..##....", "..##....", "..##....", "..##...."],
    ["..####..", ".##..##.", ".##..##.", "..####..", ".##..##.", ".##..##.", ".##..##.", "..####.."],
    ["..####..", ".##..##.", ".##..##.", ".##..##.", "..#####.", ".....##.", ".....##.", "..####.."],
]
TEMPLATES = np.array([[[1.0 if c == "#" else 0.0 for c in row] for row in g] for g in GLYPHS])


def make_digits(n, seed):
    """Noisy, shifted 8x8 renderings of ten glyphs. Returns X (n, 64) and y (n,). Do not change."""
    rng = np.random.default_rng(seed)
    y = rng.integers(0, 10, size=n)
    X = np.zeros((n, 8, 8))
    for i in range(n):
        img = TEMPLATES[y[i]]
        dx, dy = rng.integers(-1, 2, size=2)
        img = np.roll(np.roll(img, dy, axis=0), dx, axis=1)
        img = img * rng.uniform(0.7, 1.0) * (rng.uniform(size=(8, 8)) > 0.1)
        X[i] = img + 0.25 * rng.normal(size=(8, 8))
    return X.reshape(n, 64), y


def layernorm_forward(x, gamma, beta, eps=1e-5):
    """Normalize each example (row) over its features, then scale and shift. Return (y, cache)."""
    mu = x.mean(axis=1, keepdims=True)
    var = x.var(axis=1, keepdims=True)
    r = 1.0 / np.sqrt(var + eps)
    xh = (x - mu) * r
    return gamma * xh + beta, (xh, r, gamma)


def layernorm_backward(dy, cache):
    """Return (dx, dgamma, dbeta)."""
    xh, r, gamma = cache
    d = dy.shape[1]
    dgamma = (dy * xh).sum(axis=0)
    dbeta = dy.sum(axis=0)
    dxh = dy * gamma
    dx = r / d * (d * dxh - dxh.sum(axis=1, keepdims=True) - xh * (dxh * xh).sum(axis=1, keepdims=True))
    return dx, dgamma, dbeta


def adam_init(p):
    return {"t": 0, "m": {k: np.zeros_like(v) for k, v in p.items()}, "v": {k: np.zeros_like(v) for k, v in p.items()}}


def adam_step(p, g, state, lr, b1=0.9, b2=0.999, eps=1e-8):
    state["t"] += 1
    t = state["t"]
    for k in p:
        state["m"][k] = b1 * state["m"][k] + (1 - b1) * g[k]
        state["v"][k] = b2 * state["v"][k] + (1 - b2) * g[k] ** 2
        p[k] -= lr * (state["m"][k] / (1 - b1 ** t)) / (np.sqrt(state["v"][k] / (1 - b2 ** t)) + eps)



DEPTH = 30


def init_model(depth, width, seed=0):
    raise NotImplementedError


def loss_and_grads(params, X, y):
    raise NotImplementedError


def train(seed=0):
    raise NotImplementedError


def evaluate(params, X, y):
    raise NotImplementedError


REPORT = """
"""
