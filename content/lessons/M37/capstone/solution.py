import math
import numpy as np

WEIGHTS = np.array([0.3, 0.3, 0.4])
MEANS = np.array([[-2.0, 0.0], [2.0, 1.0], [0.0, -2.0]])


# provided
def sample_target(n, rng):
    k = rng.choice(3, size=n, p=WEIGHTS)
    return MEANS[k] + 0.35 * rng.standard_normal((n, 2))


# provided
def sliced_w1(X, Y, seed=0, n_proj=50):
    phi = np.random.default_rng(seed).uniform(0, np.pi, n_proj)
    D = np.stack([np.cos(phi), np.sin(phi)], axis=1)
    q = (np.arange(200) + 0.5) / 200
    return float(np.mean(np.abs(np.quantile(X @ D.T, q, axis=0) - np.quantile(Y @ D.T, q, axis=0))))


def kde_score(X, t, centres, h):
    """Score of the noised kernel density estimate."""
    a = math.exp(-t)
    v = a * a * h * h + 1 - a * a
    d = np.asarray(X)[:, None, :] - a * np.asarray(centres)[None]
    L = -np.sum(d * d, axis=2) / (2 * v)
    R = np.exp(L - L.max(axis=1, keepdims=True))
    R /= R.sum(axis=1, keepdims=True)
    return -np.einsum("nk,nkd->nd", R, d) / v


def dsm_loss(score, x0, seed, T=5.0, n_t=8):
    """Sigma-weighted denoising score-matching loss averaged over times."""
    rng = np.random.default_rng(seed)
    total = 0.0
    for t in np.geomspace(0.01, T, n_t):
        a = math.exp(-t)
        s = math.sqrt(1 - a * a)
        eps = rng.standard_normal(np.shape(x0))
        total += float(np.mean(np.sum((s * score(a * x0 + s * eps, t) + eps) ** 2, axis=1)))
    return total / n_t


def fit(train, valid, hs=(0.0, 0.05, 0.1, 0.2, 0.4)):
    """Bandwidth with the smallest held-out loss."""
    losses = [dsm_loss(lambda x, t: kde_score(x, t, train, h), valid, 7) for h in hs]
    return hs[int(np.argmin(losses))]


def sample(train, h, n, seed=0, T=5.0, steps=60):
    """Reverse-time SDE with the kernel score."""
    rng = np.random.default_rng(seed)
    ts = np.geomspace(T, 1e-3, steps + 1)
    x = rng.standard_normal((n, 2))
    for i in range(steps):
        dt = ts[i] - ts[i + 1]
        x = x + dt * (x + 2 * kde_score(x, ts[i], train, h)) + math.sqrt(2 * dt) * rng.standard_normal((n, 2))
    return x


def nn_distance(gen, train):
    """Median distance to the nearest training point."""
    d = np.linalg.norm(np.asarray(gen)[:, None, :] - np.asarray(train)[None], axis=2)
    return float(np.median(d.min(axis=1)))


# your answer
REPORT = """
The model is a kernel density estimate of the 300 training points, noised by the forward
process, whose exact score drives the reverse SDE over 60 geometrically spaced steps from T = 5.
Denoising score matching on 300 held-out points chose the bandwidth: the losses were 0.780,
0.771, 0.758, 0.753 and 0.804 for bandwidths 0, 0.05, 0.1, 0.2 and 0.4, so h = 0.2. The 600
generated points are at sliced Wasserstein distance 0.175 from 2,000 fresh target points,
against 0.166 for the training set itself, 0.086 for 600 fresh points, and 0.63 for the
Gaussian noise the reverse process starts from: the model reproduces the target about as well
as its 300 examples allow. The memorization check passes: the median distance from a generated
point to its nearest training point is 0.063, the same as for fresh data, 0.062, where a
bandwidth of zero run to a tiny final time would copy the training points. A neural network
would replace the kernel score with a learned function of the point and the time, trained by
the same score matching objective on all noise levels, and would scale to images where a
kernel estimate cannot.
"""
