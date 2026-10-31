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


class SGD:
    """SGD with optional heavy-ball momentum and L2 weight decay on the weights (keys starting with "W")."""

    def __init__(self, lr, momentum=0.0, weight_decay=0.0):
        self.lr, self.momentum, self.weight_decay = lr, momentum, weight_decay
        self.v = {}

    def step(self, params, grads, lr=None):
        lr = self.lr if lr is None else lr
        for k in params:
            g = grads[k]
            if self.weight_decay and k.startswith("W"):
                g = g + self.weight_decay * params[k]
            if self.momentum:
                self.v[k] = self.momentum * self.v.get(k, 0.0) + g
                g = self.v[k]
            params[k] -= lr * g


class Adam:
    """Adam on a dict of arrays. weight_decay applies to the weights only, either decoupled
    (AdamW) or as an L2 term added to the gradient."""

    def __init__(self, lr, b1=0.9, b2=0.999, eps=1e-8, weight_decay=0.0, decoupled=True, bias_correction=True):
        self.lr, self.b1, self.b2, self.eps = lr, b1, b2, eps
        self.weight_decay, self.decoupled, self.bias_correction = weight_decay, decoupled, bias_correction
        self.m, self.v, self.t = {}, {}, 0

    def step(self, params, grads, lr=None):
        lr = self.lr if lr is None else lr
        self.t += 1
        c1 = 1.0 - self.b1 ** self.t if self.bias_correction else 1.0
        c2 = 1.0 - self.b2 ** self.t if self.bias_correction else 1.0
        for k in params:
            g = grads[k]
            wd = self.weight_decay if k.startswith("W") else 0.0
            if wd and not self.decoupled:
                g = g + wd * params[k]
            self.m[k] = self.b1 * self.m.get(k, 0.0) + (1.0 - self.b1) * g
            self.v[k] = self.b2 * self.v.get(k, 0.0) + (1.0 - self.b2) * g * g
            if wd and self.decoupled:
                params[k] -= lr * wd * params[k]
            params[k] -= lr * (self.m[k] / c1) / (np.sqrt(self.v[k] / c2) + self.eps)


def train(opt, X, y, steps, batch=50, schedule=None, seed=0, sizes=(64, 64, 32, 10)):
    """Minibatch training of init(sizes, seed) with `opt`. Each epoch visits a fresh permutation
    in full batches. If schedule is given, step t (1-based) uses lr = schedule(t).
    Return (params, losses) with the minibatch loss of every step."""
    params = init(list(sizes), seed)
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    losses = []
    t = 0
    while t < steps:
        perm = rng.permutation(n)
        for i in range(0, n - batch + 1, batch):
            if t == steps:
                break
            t += 1
            idx = perm[i:i + batch]
            loss, g = loss_and_grads(params, X[idx], y[idx])
            losses.append(loss)
            opt.step(params, g, None if schedule is None else schedule(t))
    return params, losses
