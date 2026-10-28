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


def init(sizes, seed=0):
    rng = np.random.default_rng(seed)
    p = {}
    for i, (a, b) in enumerate(zip(sizes, sizes[1:]), start=1):
        p[f"W{i}"] = rng.normal(size=(a, b)) * np.sqrt(2.0 / a)
        p[f"b{i}"] = np.zeros(b)
    return p


def _forward(p, X):
    L = len(p) // 2
    h, cache = X, []
    for i in range(1, L + 1):
        z = h @ p[f"W{i}"] + p[f"b{i}"]
        cache.append((h, z))
        h = np.maximum(z, 0) if i < L else z
    return h, cache


def loss_and_grads(params, X, y):
    Z, cache = _forward(params, X)
    L = len(params) // 2
    B = X.shape[0]
    Zs = Z - Z.max(axis=1, keepdims=True)
    logp = Zs - np.log(np.exp(Zs).sum(axis=1, keepdims=True))
    loss = -np.mean(logp[np.arange(B), y])
    G = np.exp(logp)
    G[np.arange(B), y] -= 1.0
    G /= B
    g = {}
    for i in range(L, 0, -1):
        h, z = cache[i - 1]
        if i < L:
            G = G * (z > 0)
        g[f"W{i}"] = h.T @ G
        g[f"b{i}"] = G.sum(axis=0)
        G = G @ params[f"W{i}"].T
    return float(loss), g


def evaluate(params, X, y):
    return float(np.mean(_forward(params, X)[0].argmax(axis=1) == y))


def loss_and_grads_l2(params, X, y, lam):
    """The L07 loss plus lam/2 times the squared norm of every weight matrix (not the biases)."""
    raise NotImplementedError


def global_norm(grads):
    """sqrt of the sum of squares of every entry of every gradient."""
    raise NotImplementedError


def clip_by_global_norm(grads, max_norm):
    """Scale all gradients by one factor so that their global norm is at most max_norm."""
    raise NotImplementedError
