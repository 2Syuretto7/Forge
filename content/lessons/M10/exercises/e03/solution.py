def _parts(s1, s2):
    vec = len(s2) == 1
    s2 = (s2[0], 1) if vec else s2
    a = (1,) + tuple(s1) if len(s1) == 2 else tuple(s1)
    b = (1,) + tuple(s2) if len(s2) == 2 else tuple(s2)
    if a[2] != b[1]:
        raise ValueError(f"inner sizes differ: {s1} @ {s2}")
    if a[0] != b[0] and 1 not in (a[0], b[0]):
        raise ValueError(f"batch sizes clash: {s1} @ {s2}")
    batch = max(a[0], b[0])
    return vec, batch, a[1], a[2], b[2], len(s1) == 3 or len(s2) == 3


def matmul_shape(s1, s2):
    """Shape of A @ B."""
    vec, batch, m, n, p, batched = _parts(s1, s2)
    out = (batch, m, p) if batched else (m, p)
    return out[:-1] if vec else out


def matmul_flops(s1, s2):
    """2 m n p per product, times the batch size."""
    vec, batch, m, n, p, batched = _parts(s1, s2)
    return 2 * m * n * p * batch
