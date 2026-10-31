import math
import numpy as np


def _seq(carry, x, dtype):
    return np.cumsum(np.concatenate([np.array([carry], dtype=dtype), x.astype(dtype)]), dtype=dtype)[-1]


def stream_sums(n_chunks=100, chunk=10**6, seed=0):
    """Running totals of 10^8 uniform float32 numbers by six methods."""
    rng = np.random.default_rng(seed)
    width = 10000
    s16, s32, s64 = np.float16(0), np.float32(0), np.float64(0)
    ks = np.zeros(width, dtype=np.float32)
    kc = np.zeros(width, dtype=np.float32)
    totals, exact = [], []
    for _ in range(n_chunks):
        x = rng.random(chunk, dtype=np.float32)
        s16 = _seq(s16, x[:4096], np.float16) if s16 < 2048 else s16
        s32 = _seq(s32, x, np.float32)
        s64 = _seq(s64, x, np.float64)
        totals.append(np.sum(x))
        exact.append(float(np.sum(x.astype(np.float64))))
        for r in x.reshape(-1, width):
            y = r - kc
            t = ks + y
            kc = (t - ks) - y
            ks = t
    tot = np.array(totals, dtype=np.float32)
    while len(tot) > 1:
        if len(tot) % 2:
            tot = np.append(tot, np.float32(0))
        tot = tot[0::2] + tot[1::2]
    s, c = np.float32(0), np.float32(0)
    for v in ks - kc:
        y = np.float32(v) - c
        t = s + y
        c = (t - s) - y
        s = t
    return {
        "float16": float(s16),
        "float32": float(s32),
        "float64": float(s64),
        "pairwise32": float(tot[0]),
        "kahan32": float(s),
        "exact": math.fsum(exact),
    }


def errors(sums):
    """Absolute error of each method against the exact sum."""
    return {k: abs(v - sums["exact"]) for k, v in sums.items() if k != "exact"}
