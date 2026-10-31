import numpy as np
import sub

rng = np.random.default_rng(5)
P = 2 ** 31 - 1
a, b = rng.integers(1, P, 128), rng.integers(0, P, 128)


def sig(ids):
    x = np.asarray(sorted(ids), dtype=np.int64)
    return ((np.outer(a, x) + b[:, None]) % P).min(axis=1)


bases = [set(rng.integers(0, 10 ** 9, 300).tolist()) for _ in range(6)]
docs = []
for i, s in enumerate(bases):
    docs.append(s)
    if i % 2 == 0:
        near = set(list(s)[:290]) | set(rng.integers(0, 10 ** 9, 10).tolist())
        docs.append(near)
sigs = [sig(d) for d in docs]


def test_candidates_find_near_copies():
    pairs = sub.lsh_candidates(sigs, 16, 8)
    assert (0, 1) in pairs and (3, 4) in pairs and (6, 7) in pairs
    assert all(i < j for i, j in pairs) and pairs == sorted(pairs)


def test_dedup_keeps_one_per_cluster():
    keep = sub.dedup_keep(sigs, 16, 8, 0.8)
    assert keep == [0, 2, 3, 5, 6, 8]
