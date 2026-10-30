def is_prime(n):
    """True when n is prime (trial division)."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def first_composite(poly, start=0):
    """First n >= start with poly(n) not prime."""
    n = start
    while is_prime(poly(n)):
        n += 1
    return n


def prime_count(poly, N):
    """How many of poly(0..N-1) are prime."""
    return sum(1 for n in range(N) if is_prime(poly(n)))


def factor_pair(m):
    """(smallest divisor d > 1, m // d) of a composite m."""
    d = 2
    while d * d <= m:
        if m % d == 0:
            return d, m // d
        d += 1
    raise ValueError(f"{m} is prime")
