import numpy as np


def pca(X, k):
    """X: (n, d). Return dict with mean, components (k, d), explained_variance (k,),
    explained_variance_ratio (k,), scores (n, k)."""
    X = np.asarray(X, dtype=float)
    n = X.shape[0]
    mean = X.mean(axis=0)
    Xc = X - mean
    _, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    comps = Vt[:k].copy()
    idx = np.argmax(np.abs(comps), axis=1)
    comps *= np.sign(comps[np.arange(k), idx])[:, None]
    var = s ** 2
    return {
        "mean": mean,
        "components": comps,
        "explained_variance": var[:k] / (n - 1),
        "explained_variance_ratio": var[:k] / var.sum(),
        "scores": Xc @ comps.T,
    }
