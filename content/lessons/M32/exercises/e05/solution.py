import math
from fractions import Fraction


def riffle(deck, rng):
    """One Gilbert-Shannon-Reeds riffle shuffle."""
    n = len(deck)
    c = int(rng.binomial(n, 0.5))
    left, right = list(deck[:c]), list(deck[c:])
    out = []
    i = j = 0
    while i < len(left) or j < len(right):
        a, b = len(left) - i, len(right) - j
        if rng.random() < a / (a + b):
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out


def rising_sequences(perm):
    """Number of rising sequences of a deck of cards 0..n-1."""
    pos = {c: i for i, c in enumerate(perm)}
    return 1 + sum(1 for c in range(len(perm) - 1) if pos[c + 1] < pos[c])


def eulerian_counts(n):
    """Number of permutations of n with r rising sequences, for r = 1..n."""
    row = {1: 1}
    for m in range(2, n + 1):
        row = {r: r * row.get(r, 0) + (m - r + 1) * row.get(r - 1, 0) for r in range(1, m + 1)}
    return row


def tv_after(k, n=52):
    """Exact total variation distance from uniform after k riffles."""
    A = eulerian_counts(n)
    u = Fraction(1, math.factorial(n))
    a = 2**k
    total = sum(A[r] * abs(Fraction(math.comb(a + n - r, n), a**n) - u) for r in range(1, n + 1))
    return float(total / 2)
