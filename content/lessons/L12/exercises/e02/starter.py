import numpy as np

import zlib

PRIME = 2 ** 31 - 1


def make_hashes(num_perm, seed=0):
    """Coefficients (a, b) of num_perm hash functions h(x) = (a x + b) mod PRIME."""
    rng = np.random.default_rng(seed)
    return rng.integers(1, PRIME, num_perm), rng.integers(0, PRIME, num_perm)


def shingle_ids(sh):
    """Each shingle as a 32-bit integer (CRC-32 of its UTF-8 bytes)."""
    return np.array(sorted(zlib.crc32(s.encode("utf-8")) for s in sh), dtype=np.int64)


def minhash(ids, a, b):
    """The MinHash signature: for each hash function i, the minimum over the shingle ids x of
    (a[i] x + b[i]) mod PRIME. ids are taken mod PRIME first."""
    raise NotImplementedError


def estimate_jaccard(sig1, sig2):
    """The fraction of positions where two signatures agree."""
    raise NotImplementedError
