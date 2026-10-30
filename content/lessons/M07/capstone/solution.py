import cmath
import random


def to_complex(x):
    """[x0 + i x1, x2 + i x3, ...]."""
    return [complex(x[2 * j], x[2 * j + 1]) for j in range(len(x) // 2)]


def from_complex(z):
    """[re0, im0, re1, im1, ...]."""
    out = []
    for c in z:
        out += [c.real, c.imag]
    return out


def _freqs(n_pairs):
    d = 2 * n_pairs
    return [10000 ** (-2 * j / d) for j in range(n_pairs)]


def encode(x, m):
    """Each complex pair multiplied by e^(i m omega_j)."""
    z = to_complex(x)
    return from_complex([c * cmath.exp(1j * m * w) for c, w in zip(z, _freqs(len(z)))])


def score(q, k, m, n):
    """Real dot product of the encoded query and key."""
    return sum(a * b for a, b in zip(encode(q, m), encode(k, n)))


def score_from_offset(q, k, offset):
    """Re sum z_j conj(w_j) e^(i offset omega_j)."""
    z, w = to_complex(q), to_complex(k)
    return sum(a * b.conjugate() * cmath.exp(1j * offset * f) for a, b, f in zip(z, w, _freqs(len(z)))).real


def verify(pairs, d, seed=0):
    """Largest |score - score_from_offset| over random queries, keys and positions."""
    rnd = random.Random(seed)
    worst = 0.0
    for _ in range(pairs):
        q = [rnd.gauss(0, 1) for _ in range(d)]
        k = [rnd.gauss(0, 1) for _ in range(d)]
        m, n = rnd.randint(0, 4096), rnd.randint(0, 4096)
        worst = max(worst, abs(score(q, k, m, n) - score_from_offset(q, k, m - n)))
    return worst


# your answer
PROOF = """
Write the query and key as complex numbers z_j and w_j, one per pair of coordinates. For two vectors in
this form the real dot product is the real part of the sum of z_j times the conjugate of w_j, because
(a + ib) times (c - id) has real part ac + bd. Encoding multiplies z_j by e^(i m omega_j) and w_j by
e^(i n omega_j). The conjugate of e^(i n omega_j) is e^(-i n omega_j), so each term of the encoded sum is
z_j conj(w_j) e^(i m omega_j) e^(-i n omega_j) = z_j conj(w_j) e^(i (m - n) omega_j), by the exponent rule.
The positions enter only through m - n, so adding the same shift to both leaves every term, and hence the
score, unchanged.
"""
