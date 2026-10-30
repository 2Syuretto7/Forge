def is_prime(n):
    """True when n is prime (trial division)."""
    raise NotImplementedError


def first_composite(poly, start=0):
    """First n >= start with poly(n) not prime."""
    raise NotImplementedError


def prime_count(poly, N):
    """How many of poly(0..N-1) are prime."""
    raise NotImplementedError


def factor_pair(m):
    """(smallest divisor d > 1, m // d) of a composite m."""
    raise NotImplementedError
