import math
import random

STATEMENTS = {
    "even_sum": "The sum of two even numbers is even. Case: a pair (a, b).",
    "square_even": "If n^2 is even then n is even. Case: an integer n.",
    "root2": "No fraction p/q equals the square root of 2. Case: a positive integer q, testing every p.",
    "cube_minus": "n^3 - n is divisible by 6. Case: an integer n.",
    "odd_product": "The product of two odd numbers is odd. Case: a pair (a, b).",
    "new_prime": "Every prime factor of n! + 1 is larger than n. Case: an integer n from 1 to 12.",
    "odd_sum": "1 + 3 + ... + (2n - 1) = n^2. Case: an integer n >= 0.",
    "distributive": "A and (B or C) = (A and B) or (A and C) for sets. Case: a triple of sets (A, B, C).",
    "de_morgan": "Not (for every x, P(x)) equals (there is x with not P(x)). Case: a dict from 0..9 to booleans.",
    "triangle": "|a + b| <= |a| + |b|. Case: a pair of real numbers (a, b).",
}


# provided
def smallest_prime_factor(m):
    """Smallest prime factor of m >= 2 by trial division."""
    d = 2
    while d * d <= m:
        if m % d == 0:
            return d
        d += 1
    return m


PREDICATES = {
    "even_sum": lambda c: (2 * c[0] + 2 * c[1]) % 2 == 0,
    "square_even": lambda n: (n * n) % 2 == 1 or n % 2 == 0,
    "root2": lambda q: all(p * p != 2 * q * q for p in range(1, 2 * q + 1)),
    "cube_minus": lambda n: (n ** 3 - n) % 6 == 0,
    "odd_product": lambda c: ((2 * c[0] + 1) * (2 * c[1] + 1)) % 2 == 1,
    "new_prime": lambda n: smallest_prime_factor(math.factorial(n) + 1) > n,
    "odd_sum": lambda n: sum(range(1, 2 * n, 2)) == n * n,
    "distributive": lambda c: c[0] & (c[1] | c[2]) == (c[0] & c[1]) | (c[0] & c[2]),
    "de_morgan": lambda t: (not all(t.values())) == any(not v for v in t.values()),
    "triangle": lambda c: abs(c[0] + c[1]) <= abs(c[0]) + abs(c[1]),
}

# your answer
PROOFS = {
    "even_sum": None,
    "square_even": None,
    "root2": None,
    "cube_minus": None,
    "odd_product": None,
    "new_prime": None,
    "odd_sum": None,
    "distributive": None,
    "de_morgan": None,
    "triangle": None,
}

# your answer
METHODS = {
    "even_sum": None,
    "square_even": None,
    "root2": None,
    "cube_minus": None,
    "odd_product": None,
    "new_prime": None,
    "odd_sum": None,
    "distributive": None,
    "de_morgan": None,
    "triangle": None,
}


def stress(predicate, cases):
    """First case where predicate is False, or None."""
    raise NotImplementedError
