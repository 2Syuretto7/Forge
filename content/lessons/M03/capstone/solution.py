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
    "even_sum": "Let the two even numbers be 2a and 2b for integers a and b, which is what being even means. Their sum is 2a + 2b = 2(a + b) by the distributive law, and a + b is an integer, so the sum is twice an integer, which is the definition of even. This covers every pair of even numbers at once.",
    "square_even": "We prove the contrapositive: if n is odd then n^2 is odd. An odd n can be written 2k + 1 for an integer k. Then n^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1, which is one more than twice an integer, so it is odd. A statement and its contrapositive are equivalent, so if n^2 is even then n is even.",
    "root2": "Suppose for contradiction that p/q = sqrt(2) with the fraction in lowest terms. Then p^2 = 2q^2, so p^2 is even, so p is even by the previous statement; write p = 2k. Then 4k^2 = 2q^2 gives q^2 = 2k^2, so q is even as well. Now p and q share the factor 2, contradicting lowest terms, so no such fraction exists.",
    "cube_minus": "Factor n^3 - n = (n - 1) n (n + 1), a product of three consecutive integers. Among any two consecutive integers one is even, so the product is divisible by 2. Among any three consecutive integers one is a multiple of 3, since the remainders mod 3 run through 0, 1 and 2. Being divisible by 2 and by 3, which share no factor, the product is divisible by 6 for every integer n.",
    "odd_product": "Write the odd numbers as 2a + 1 and 2b + 1 with integers a and b. Their product is 4ab + 2a + 2b + 1 = 2(2ab + a + b) + 1. That is twice an integer plus one, which is the definition of an odd number. Since a and b were arbitrary integers, this holds for every pair of odd numbers.",
    "new_prime": "Let p be a prime factor of n! + 1 and suppose for contradiction that p <= n. Then p divides n! because n! is the product of all numbers from 1 to n. So p divides the difference (n! + 1) - n! = 1, which is impossible for a prime, since primes are at least 2. Hence every prime factor of n! + 1 is larger than n, so there is always a prime above n.",
    "odd_sum": "Directly: write the sum of the first n odd numbers twice, once forwards and once backwards, and add the two rows term by term. Each column is (2k - 1) + (2(n - k + 1) - 1) = 2n, and there are n columns, so twice the sum is 2n times n. Dividing by two, the sum is n^2. This argument works for every n, including n = 0 where both sides are 0.",
    "distributive": "We show each side is contained in the other by cases on an element x. If x is in A and (B or C), then x is in A and in B, or in A and in C, so it is in the right side. Conversely, if x is in A and B, or in A and C, then x is in A and in B or C. Both inclusions hold for every element, so the two sets are equal.",
    "de_morgan": "By cases. If every P(x) is true, the left side is false, and there is no x with not P(x), so the right side is false too. If some P(x) is false, the left side is true, and that x is a witness with not P(x), so the right side is true. These cases cover every possibility, so the two statements always have the same truth value.",
    "triangle": "By cases on signs. If a and b have the same sign, |a + b| = |a| + |b| exactly, since the sizes add. If they have opposite signs, part of one cancels the other, so |a + b| equals the difference of |a| and |b|, which is at most their sum. Every pair of real numbers falls into one of these cases, so the inequality always holds.",
}

# your answer
METHODS = {
    "even_sum": "direct",
    "square_even": "contrapositive",
    "root2": "contradiction",
    "cube_minus": "cases",
    "odd_product": "direct",
    "new_prime": "contradiction",
    "odd_sum": "direct",
    "distributive": "cases",
    "de_morgan": "cases",
    "triangle": "cases",
}


def stress(predicate, cases):
    """First case where predicate is False, or None."""
    for c in cases:
        if not predicate(c):
            return c
    return None
