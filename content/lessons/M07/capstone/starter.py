import cmath
import random


def to_complex(x):
    """[x0 + i x1, x2 + i x3, ...]."""
    raise NotImplementedError


def from_complex(z):
    """[re0, im0, re1, im1, ...]."""
    raise NotImplementedError


def _freqs(n_pairs):
    raise NotImplementedError


def encode(x, m):
    """Each complex pair multiplied by e^(i m omega_j)."""
    raise NotImplementedError


def score(q, k, m, n):
    """Real dot product of the encoded query and key."""
    raise NotImplementedError


def score_from_offset(q, k, offset):
    """Re sum z_j conj(w_j) e^(i offset omega_j)."""
    raise NotImplementedError


def verify(pairs, d, seed=0):
    """Largest |score - score_from_offset| over random queries, keys and positions."""
    raise NotImplementedError


# your answer
PROOF = """
"""
