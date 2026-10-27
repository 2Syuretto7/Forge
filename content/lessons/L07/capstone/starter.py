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
    raise NotImplementedError


def loss_and_grads(params, X, y):
    raise NotImplementedError


def train(X, y, seed=0):
    raise NotImplementedError


def evaluate(params, X, y):
    raise NotImplementedError


REPORT = """
"""
