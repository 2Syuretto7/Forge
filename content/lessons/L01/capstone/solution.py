import numpy as np

GROUPS = ["science", "finance", "music", "sports", "politics", "travel"]


def make_embeddings(seed=0, n=1500):
    """Synthetic embeddings: six named feature groups, three strong latent factors,
    three weak ones, and isotropic noise. Returns X (n, 48) and the feature names."""
    rng = np.random.default_rng(seed)
    d_per = 8
    names = [f"{g}_{i}" for g in GROUPS for i in range(d_per)]
    stds = [3.0, 2.0, 1.5, 0.6, 0.45, 0.35]
    X = np.zeros((n, len(names)))
    for gi, sd in enumerate(stds):
        w = 1.0 + 0.2 * rng.normal(size=d_per)
        w /= np.linalg.norm(w)
        z = sd * rng.normal(size=n)
        X[:, gi * d_per:(gi + 1) * d_per] += np.outer(z, w)
    X += 0.1 * rng.normal(size=X.shape)
    X += 0.5 * rng.normal(size=len(names))
    return X, names


def fit_pca(X):
    """Return (mean (d,), components (d, d) as rows, ratios (d,) descending)."""
    mean = X.mean(axis=0)
    _, s, Vt = np.linalg.svd(X - mean, full_matrices=False)
    idx = np.argmax(np.abs(Vt), axis=1)
    Vt = Vt * np.sign(Vt[np.arange(Vt.shape[0]), idx])[:, None]
    ratios = s ** 2 / np.sum(s ** 2)
    return mean, Vt, ratios


def k_for_variance(ratios, target=0.95):
    """Smallest k with sum(ratios[:k]) >= target."""
    c = np.cumsum(ratios)
    return int(np.argmax(c >= target - 1e-12)) + 1


def reconstruct(X, mean, components, k):
    """Project X onto the top-k components and map back. Return (n, d)."""
    Vk = components[:k]
    return (X - mean) @ Vk.T @ Vk + mean


def top_groups(components, names, top=3):
    """For each of the first `top` components, the group with the largest share of squared loadings."""
    groups = [n.split("_")[0] for n in names]
    order = list(dict.fromkeys(groups))
    out = []
    for c in components[:top]:
        share = {g: 0.0 for g in order}
        for g, w in zip(groups, c):
            share[g] += w * w
        out.append(max(order, key=lambda g: share[g]))
    return out


REPORT = """
Four principal components reach 95 percent of the variance: the cumulative ratios are about
0.55, 0.79, 0.93 and 0.95. The first component loads almost entirely on the science features,
so it measures how strongly a point expresses the science factor. The second loads on the
finance features and the third on the music features; each is close to a uniform weighting
of its eight dimensions, which matches a single latent factor per group. Together these three
explain about 93 percent of the variance. The fourth to sixth components pick up the much
weaker sports, politics and travel factors, and everything after that is isotropic noise
spread evenly over all 48 dimensions, with tiny and nearly equal variance per direction.
"""
