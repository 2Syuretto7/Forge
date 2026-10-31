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


MODES = ("plain", "plain_ln", "res", "pre", "post")


def init_stack(depth, width, seed=0, d_in=64, d_out=10, branch_scale=1.0):
    """Input projection, `depth` hidden layers (W{l} with He init times branch_scale, and a layer
    norm's g{l}, b{l}), a final norm (gf, bf, used by pre-norm) and an output projection."""
    rng = np.random.default_rng(seed)
    p = {"Win": rng.normal(size=(d_in, width)) * np.sqrt(1.0 / d_in)}
    for l in range(depth):
        p[f"W{l}"] = rng.normal(size=(width, width)) * np.sqrt(2.0 / width) * branch_scale
        p[f"g{l}"] = np.ones(width)
        p[f"b{l}"] = np.zeros(width)
    p["gf"], p["bf"] = np.ones(width), np.zeros(width)
    p["Wout"] = rng.normal(size=(width, d_out)) * np.sqrt(1.0 / width)
    return p


def stack_forward(p, X, depth, mode):
    """Return (logits, hidden, caches). Layer l, with F(u) = relu(u W{l}) and LN the layer norm:
    plain: h <- F(h); plain_ln: h <- F(LN(h)); res: h <- h + F(h);
    pre: h <- h + F(LN(h)), with a final LN before Wout; post: h <- LN(h + F(h))."""
    h = X @ p["Win"]
    caches = []
    for l in range(depth):
        W, g, b = p[f"W{l}"], p[f"g{l}"], p[f"b{l}"]
        if mode in ("plain_ln", "pre"):
            u, c = layernorm_forward(h, g, b)
        else:
            u, c = h, None
        z = u @ W
        f = np.maximum(z, 0.0)
        caches.append((u, z, c))
        if mode in ("plain", "plain_ln"):
            h = f
        elif mode in ("res", "pre"):
            h = h + f
        else:
            h, c2 = layernorm_forward(h + f, g, b)
            caches[-1] = (u, z, c2)
    if mode == "pre":
        h, c = layernorm_forward(h, p["gf"], p["bf"])
        caches.append(c)
    return h @ p["Wout"], h, caches


def stack_loss_and_grads(p, X, y, depth, mode):
    """Mean softmax cross-entropy and the gradient of every parameter (zeros for unused ones)."""
    logits, hL, caches = stack_forward(p, X, depth, mode)
    B = X.shape[0]
    Z = logits - logits.max(axis=1, keepdims=True)
    logp = Z - np.log(np.exp(Z).sum(axis=1, keepdims=True))
    loss = -float(np.mean(logp[np.arange(B), y]))
    G = np.exp(logp)
    G[np.arange(B), y] -= 1.0
    G /= B
    g = {k: np.zeros_like(v) for k, v in p.items()}
    g["Wout"] = hL.T @ G
    dh = G @ p["Wout"].T
    if mode == "pre":
        dh, g["gf"], g["bf"] = layernorm_backward(dh, caches[depth])
    for l in range(depth - 1, -1, -1):
        u, z, c = caches[l]
        W = p[f"W{l}"]
        if mode == "post":
            dh, g[f"g{l}"], g[f"b{l}"] = layernorm_backward(dh, c)
        df = dh
        dz = df * (z > 0)
        g[f"W{l}"] = u.T @ dz
        du = dz @ W.T
        if mode in ("plain_ln", "pre"):
            du, g[f"g{l}"], g[f"b{l}"] = layernorm_backward(du, c)
        dh = du if mode in ("plain", "plain_ln") else dh + du
    g["Win"] = X.T @ dh
    return loss, g
