import math
from fractions import Fraction
import numpy as np
import sub


def test_famous_table():
    got = [round(sub.tv_after(k), 3) for k in range(5, 11)]
    assert got == [0.924, 0.614, 0.334, 0.167, 0.085, 0.043], got
    assert min(k for k in range(1, 20) if sub.tv_after(k) < 0.5) == 7


def test_counts():
    A = sub.eulerian_counts(6)
    assert [A[r] for r in range(1, 7)] == [1, 57, 302, 302, 57, 1]
    assert sum(sub.eulerian_counts(10).values()) == math.factorial(10)
    assert sub.rising_sequences([0, 1, 2, 3]) == 1 and sub.rising_sequences([3, 2, 1, 0]) == 4
    assert sub.rising_sequences([0, 2, 1, 3]) == 2


def test_simulation_matches_formula():
    rng = np.random.default_rng(0)
    n, k, T = 8, 3, 10000
    counts = {}
    for _ in range(T):
        d = list(range(n))
        for _ in range(k):
            d = sub.riffle(d, rng)
        assert sorted(d) == list(range(n))
        r = sub.rising_sequences(d)
        counts[r] = counts.get(r, 0) + 1
    A = sub.eulerian_counts(n)
    for r in range(1, n + 1):
        p = float(A[r] * Fraction(math.comb(2**k + n - r, n), 2 ** (k * n)))
        assert abs(counts.get(r, 0) / T - p) < 0.015, (r, counts.get(r, 0) / T, p)
