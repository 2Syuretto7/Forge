import numpy as np


def ring_allreduce(xs):
    """Simulate a ring all-reduce over P ranks, each holding one array in xs. Split every array into
    P chunks (np.array_split). Reduce-scatter: in step s = 0 .. P-2, every rank r sends its chunk
    (r - s) mod P to rank r + 1, which adds it to its own. All-gather: in step s, every rank r sends
    its chunk (r + 1 - s) mod P to rank r + 1, which replaces its own. All sends in a step happen at
    once. Return (the P resulting arrays, the number of elements each rank sent)."""
    raise NotImplementedError
