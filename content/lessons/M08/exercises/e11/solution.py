import math

import numpy as np


def expected_colliding_pairs(n, bits):
    """C(n, 2) / 2**bits."""
    return math.comb(n, 2) / 2 ** bits


def p_any_collision(n, bits):
    """1 - exp(-C(n, 2) / 2**bits)."""
    return 1 - math.exp(-expected_colliding_pairs(n, bits))


def simulated_colliding_pairs(n, bits, seed=0):
    """Colliding pairs among n uniform random hash values of the given width."""
    v = np.random.default_rng(seed).integers(0, 2 ** bits, size=n, dtype=np.int64)
    _, counts = np.unique(v, return_counts=True)
    return int(np.sum(counts * (counts - 1) // 2))
