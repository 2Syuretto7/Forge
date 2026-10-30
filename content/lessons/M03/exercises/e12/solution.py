def sieve(n):
    """Primes up to and including n."""
    if n < 2:
        return []
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    p = 2
    while p * p <= n:
        if is_p[p]:
            for k in range(p * p, n + 1, p):
                is_p[k] = False
        p += 1
    return [k for k in range(n + 1) if is_p[k]]


def race(n):
    """(primes <= n with remainder 1 mod 4, primes <= n with remainder 3 mod 4)."""
    ps = sieve(n)
    return sum(1 for p in ps if p % 4 == 1), sum(1 for p in ps if p % 4 == 3)


def first_lead_change(limit):
    """Smallest n <= limit where remainder-1 primes are strictly ahead, or None."""
    ones = threes = 0
    ps = set(sieve(limit))
    for n in range(limit + 1):
        if n in ps:
            if n % 4 == 1:
                ones += 1
            elif n % 4 == 3:
                threes += 1
        if ones > threes:
            return n
    return None
