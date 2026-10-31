import numpy as np


def naive_sum32(x):
    """Sequential float32 sum."""
    return float(np.cumsum(np.asarray(x, dtype=np.float32), dtype=np.float32)[-1])


def pairwise_sum32(x):
    """Pairwise float32 sum."""
    x = np.asarray(x, dtype=np.float32)
    while len(x) > 1:
        if len(x) % 2:
            x = np.append(x, np.float32(0))
        x = x[0::2] + x[1::2]
    return float(x[0])


def _kahan_rows(rows):
    s = np.zeros(rows.shape[1:], dtype=np.float32)
    c = np.zeros(rows.shape[1:], dtype=np.float32)
    for r in rows:
        y = r - c
        t = s + y
        c = (t - s) - y
        s = t
    return s


def kahan_sum32(x, width=10000):
    """Kahan float32 sum, vectorized across width running sums."""
    x = np.asarray(x, dtype=np.float32)
    pad = (-len(x)) % width
    rows = np.concatenate([x, np.zeros(pad, dtype=np.float32)]).reshape(-1, width)
    totals = _kahan_rows(rows)
    return float(_kahan_rows(totals.reshape(-1, 1))[0])
