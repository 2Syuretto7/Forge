import numpy as np


def calibration_bins(P, y, n_bins=10):
    c = P.max(axis=1)
    a = (P.argmax(axis=1) == y).astype(float)
    idx = np.clip(np.ceil(c * n_bins).astype(int) - 1, 0, n_bins - 1)
    conf = np.zeros(n_bins)
    acc = np.zeros(n_bins)
    cnt = np.zeros(n_bins, dtype=int)
    for b in range(n_bins):
        m = idx == b
        cnt[b] = int(m.sum())
        if cnt[b]:
            conf[b] = c[m].mean()
            acc[b] = a[m].mean()
    return conf, acc, cnt


def ece(P, y, n_bins=10):
    conf, acc, cnt = calibration_bins(P, y, n_bins)
    n = cnt.sum()
    return float(np.sum(cnt / n * np.abs(acc - conf)))
