def softmax_traffic(rows, cols, bytes_per=2, fused=True):
    """Bytes moved by a row softmax. Unfused (as separate operations): read x for the max, read x
    and write e = exp(x - max), read e for the sum, read e and write the result: 6 arrays. Fused:
    read x once and write the result once (the row stays on chip): 2 arrays."""
    raise NotImplementedError


def predicted_speedup(rows, cols, bytes_per=2):
    raise NotImplementedError


def fits_on_chip(cols, bytes_per=4, budget=64 * 1024):
    """Whether one row (held in fp32) fits in the per-program on-chip budget."""
    raise NotImplementedError
