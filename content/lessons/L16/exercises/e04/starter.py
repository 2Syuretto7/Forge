import numpy as np


def lsh_candidates(signatures, bands, rows):
    """Sorted list of pairs (i, j), i < j, of documents whose signatures agree on every row of at
    least one band. Bucket each band of each signature by (band index, tuple of its values)."""
    raise NotImplementedError


def dedup_keep(signatures, bands, rows, min_similarity):
    """Join candidate pairs whose signatures agree in at least min_similarity of positions into
    clusters (union-find), and return the sorted indices to keep: the smallest of each cluster."""
    raise NotImplementedError
