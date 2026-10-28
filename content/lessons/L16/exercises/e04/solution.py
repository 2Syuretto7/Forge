import numpy as np


def lsh_candidates(signatures, bands, rows):
    """Sorted list of pairs (i, j), i < j, of documents whose signatures agree on every row of at
    least one band. Bucket each band of each signature by (band index, tuple of its values)."""
    buckets = {}
    for i, sig in enumerate(signatures):
        for band in range(bands):
            key = (band, tuple(int(v) for v in sig[band * rows:(band + 1) * rows]))
            buckets.setdefault(key, []).append(i)
    pairs = set()
    for members in buckets.values():
        for x in range(len(members)):
            for y in range(x + 1, len(members)):
                pairs.add((members[x], members[y]))
    return sorted(pairs)


def dedup_keep(signatures, bands, rows, min_similarity):
    """Join candidate pairs whose signatures agree in at least min_similarity of positions into
    clusters (union-find), and return the sorted indices to keep: the smallest of each cluster."""
    parent = list(range(len(signatures)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i, j in lsh_candidates(signatures, bands, rows):
        if np.mean(np.asarray(signatures[i]) == np.asarray(signatures[j])) >= min_similarity:
            ri, rj = find(i), find(j)
            parent[max(ri, rj)] = min(ri, rj)
    return sorted({find(i) for i in range(len(signatures))})
