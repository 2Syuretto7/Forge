import numpy as np


def _cv(x, y, d, k, seed):
    perm = np.random.default_rng(seed).permutation(len(x))
    folds = np.array_split(perm, k)
    s = []
    for i in range(k):
        tr = np.concatenate([folds[j] for j in range(k) if j != i])
        va = folds[i]
        c = np.linalg.lstsq(np.vander(x[tr], d + 1, increasing=True), y[tr], rcond=None)[0]
        s.append(np.mean((np.vander(x[va], d + 1, increasing=True) @ c - y[va]) ** 2))
    return np.mean(s)


def select_degree(x, y, degrees, k=5, seed=0):
    best = None
    for d in degrees:
        s = _cv(x, y, d, k, seed)
        if best is None or s < best[0]:
            best = (s, d)
    return int(best[1])


def refit(x, y, degree):
    return np.linalg.lstsq(np.vander(x, degree + 1, increasing=True), y, rcond=None)[0]
