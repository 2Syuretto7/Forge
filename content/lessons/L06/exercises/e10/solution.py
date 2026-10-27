import numpy as np


def top_k_features(X, y, k):
    Xc = X - X.mean(axis=0)
    yc = y - y.mean()
    corr = (Xc * yc[:, None]).sum(axis=0) / (np.linalg.norm(Xc, axis=0) * np.linalg.norm(yc) + 1e-12)
    return np.argsort(-np.abs(corr))[:k]


def centroid_classifier(Xtr, ytr, Xte):
    m0 = Xtr[ytr == 0].mean(axis=0)
    m1 = Xtr[ytr == 1].mean(axis=0)
    d0 = np.sum((Xte - m0) ** 2, axis=1)
    d1 = np.sum((Xte - m1) ** 2, axis=1)
    return (d1 < d0).astype(int)


def cv_accuracy(X, y, k=20, folds=5, seed=0, leaky=False):
    perm = np.random.default_rng(seed).permutation(len(y))
    parts = np.array_split(perm, folds)
    feats_all = top_k_features(X, y, k) if leaky else None
    accs = []
    for i in range(folds):
        va = parts[i]
        tr = np.concatenate([parts[j] for j in range(folds) if j != i])
        f = feats_all if leaky else top_k_features(X[tr], y[tr], k)
        pred = centroid_classifier(X[tr][:, f], y[tr], X[va][:, f])
        accs.append(np.mean(pred == y[va]))
    return float(np.mean(accs))
