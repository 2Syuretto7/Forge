import numpy as np

GROUPS = ["science", "finance", "music", "sports", "politics", "travel"]


# provided
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
    raise NotImplementedError


def k_for_variance(ratios, target=0.95):
    """Smallest k with sum(ratios[:k]) >= target."""
    raise NotImplementedError


def reconstruct(X, mean, components, k):
    """Project X onto the top-k components and map back. Return (n, d)."""
    raise NotImplementedError


def top_groups(components, names, top=3):
    """For each of the first `top` components, the group with the largest share of squared loadings."""
    raise NotImplementedError


# your answer
REPORT = """
"""
