import numpy as np


def kfold_indices(n, k, seed=0):
    perm = np.random.default_rng(seed).permutation(n)
    folds = np.array_split(perm, k)
    out = []
    for i in range(k):
        train = np.concatenate([folds[j] for j in range(k) if j != i])
        out.append((train, folds[i]))
    return out


def cv_mse(x, y, degree, k=5, seed=0):
    scores = []
    for tr, va in kfold_indices(len(x), k, seed):
        c = np.linalg.lstsq(np.vander(x[tr], degree + 1, increasing=True), y[tr], rcond=None)[0]
        pred = np.vander(x[va], degree + 1, increasing=True) @ c
        scores.append(np.mean((pred - y[va]) ** 2))
    return float(np.mean(scores))
