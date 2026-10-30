import math


# provided
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


# provided
def fib(n):
    """The n-th Fibonacci number: fib(0) = 0, fib(1) = 1."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


CLAIMS = [
    # False claims.
    {"name": "every prime is odd", "start": 2, "claim": lambda n: not is_prime(n) or n % 2 == 1},
    {"name": "every odd number above 1 is prime", "start": 3, "claim": lambda n: n % 2 == 0 or is_prime(n)},
    {"name": "n^2 + n + 41 is prime", "start": 0, "claim": lambda n: is_prime(n * n + n + 41)},
    {"name": "n^2 - n + 41 is prime", "start": 0, "claim": lambda n: is_prime(n * n - n + 41)},
    {"name": "2^n - 1 is prime for prime n", "start": 2, "claim": lambda n: not is_prime(n) or is_prime(2 ** n - 1)},
    {"name": "2^(2^n) + 1 is prime", "start": 0, "claim": lambda n: is_prime(2 ** (2 ** n) + 1)},
    {"name": "n! + 1 is prime", "start": 1, "claim": lambda n: is_prime(math.factorial(n) + 1)},
    {"name": "2^n > n^2", "start": 1, "claim": lambda n: 2 ** n > n * n},
    {"name": "n^2 >= 2n", "start": 1, "claim": lambda n: n * n >= 2 * n},
    {"name": "n < 100", "start": 0, "claim": lambda n: n < 100},
    {"name": "6n + 1 or 6n - 1 is prime", "start": 1, "claim": lambda n: is_prime(6 * n + 1) or is_prime(6 * n - 1)},
    {"name": "n^2 + 1 is prime for even n", "start": 0, "claim": lambda n: n % 2 == 1 or is_prime(n * n + 1)},
    {"name": "3n + 1 is not a square", "start": 0, "claim": lambda n: math.isqrt(3 * n + 1) ** 2 != 3 * n + 1},
    {"name": "n^2 + n + 17 is prime", "start": 0, "claim": lambda n: is_prime(n * n + n + 17)},
    {"name": "n divides 2^n - 2 only for prime n", "start": 2, "claim": lambda n: (2 ** n - 2) % n != 0 or is_prime(n)},
    {"name": "n^2 + n + 1 is prime", "start": 1, "claim": lambda n: is_prime(n * n + n + 1)},
    {"name": "10n + 1 is prime", "start": 1, "claim": lambda n: is_prime(10 * n + 1)},
    {"name": "n and n + 2 are never both prime", "start": 2, "claim": lambda n: not (is_prime(n) and is_prime(n + 2))},
    {"name": "n^3 + 2 is prime for odd n", "start": 1, "claim": lambda n: n % 2 == 0 or is_prime(n ** 3 + 2)},
    {"name": "4n + 3 is prime", "start": 0, "claim": lambda n: is_prime(4 * n + 3)},
    {"name": "every number is a sum of at most three squares", "start": 0,
     "claim": lambda n: any(n - a * a - b * b >= 0 and math.isqrt(n - a * a - b * b) ** 2 == n - a * a - b * b
                             for a in range(math.isqrt(n) + 1) for b in range(math.isqrt(n) + 1))},
    {"name": "n^2 + 2 is not divisible by 3", "start": 0, "claim": lambda n: (n * n + 2) % 3 != 0},
    {"name": "n^5 - n is divisible by 10 only for even n", "start": 0, "claim": lambda n: (n ** 5 - n) % 10 != 0 or n % 2 == 0},
    {"name": "between n and 2n there are at least two primes", "start": 1, "claim": lambda n: sum(is_prime(k) for k in range(n + 1, 2 * n)) >= 2},
    {"name": "11...1 with n ones is not divisible by 11", "start": 1, "claim": lambda n: int("1" * n) % 11 != 0},
    # True claims.
    {"name": "n^3 - n is divisible by 6", "start": 0, "claim": lambda n: (n ** 3 - n) % 6 == 0},
    {"name": "1 + 3 + ... + (2n - 1) = n^2", "start": 0, "claim": lambda n: sum(range(1, 2 * n, 2)) == n * n},
    {"name": "n^2 leaves remainder 0 or 1 mod 4", "start": 0, "claim": lambda n: n * n % 4 in (0, 1)},
    {"name": "n(n + 1)(n + 2) is divisible by 6", "start": 0, "claim": lambda n: n * (n + 1) * (n + 2) % 6 == 0},
    {"name": "1 + 2 + ... + n = n(n + 1)/2", "start": 0, "claim": lambda n: 2 * sum(range(n + 1)) == n * (n + 1)},
    {"name": "n^2 + 1 is not divisible by 3", "start": 0, "claim": lambda n: (n * n + 1) % 3 != 0},
    {"name": "n^5 - n is divisible by 5", "start": 0, "claim": lambda n: (n ** 5 - n) % 5 == 0},
    {"name": "2^n >= n + 1", "start": 0, "claim": lambda n: 2 ** n >= n + 1},
    {"name": "n! >= 2^(n - 1)", "start": 1, "claim": lambda n: math.factorial(n) >= 2 ** (n - 1)},
    {"name": "there is a prime between n and 2n", "start": 1, "claim": lambda n: any(is_prime(k) for k in range(n + 1, 2 * n + 1))},
    {"name": "every number above 1 has a prime divisor", "start": 2, "claim": lambda n: any(n % d == 0 and is_prime(d) for d in range(2, n + 1))},
    {"name": "the sum of the digits of 9n is divisible by 9", "start": 0, "claim": lambda n: sum(map(int, str(9 * n))) % 9 == 0},
    {"name": "n^2 - n is even", "start": 0, "claim": lambda n: (n * n - n) % 2 == 0},
    {"name": "every number is a sum of four squares", "start": 0,
     "claim": lambda n: any(math.isqrt(n - a * a - b * b - c * c) ** 2 == n - a * a - b * b - c * c
                             for a in range(math.isqrt(n) + 1) for b in range(math.isqrt(n) + 1) for c in range(math.isqrt(n) + 1)
                             if n - a * a - b * b - c * c >= 0)},
    {"name": "gcd(n, n + 1) = 1", "start": 0, "claim": lambda n: math.gcd(n, n + 1) == 1},
    {"name": "3^n - 1 is even", "start": 0, "claim": lambda n: (3 ** n - 1) % 2 == 0},
    {"name": "7^n - 1 is divisible by 6", "start": 0, "claim": lambda n: (7 ** n - 1) % 6 == 0},
    {"name": "n^3 + 2n is divisible by 3", "start": 0, "claim": lambda n: (n ** 3 + 2 * n) % 3 == 0},
    {"name": "the last digit of n^4 is 0, 1, 5 or 6", "start": 0, "claim": lambda n: n ** 4 % 10 in (0, 1, 5, 6)},
    {"name": "1^3 + ... + n^3 = (1 + ... + n)^2", "start": 0, "claim": lambda n: sum(k ** 3 for k in range(n + 1)) == sum(range(n + 1)) ** 2},
    {"name": "fib(n) and fib(n + 1) share no factor", "start": 0, "claim": lambda n: math.gcd(fib(n), fib(n + 1)) == 1},
    {"name": "n^2 + n is even", "start": 0, "claim": lambda n: (n * n + n) % 2 == 0},
    {"name": "a prime above 3 leaves remainder 1 or 5 mod 6", "start": 4, "claim": lambda n: not is_prime(n) or n % 6 in (1, 5)},
    {"name": "8 divides n^2 - 1 for odd n", "start": 0, "claim": lambda n: n % 2 == 0 or (n * n - 1) % 8 == 0},
    {"name": "the product of n consecutive numbers is divisible by n!", "start": 1,
     "claim": lambda n: math.prod(range(5, 5 + n)) % math.factorial(n) == 0},
]


def hunt_count(claim, cases):
    """(first counterexample or None, number of cases tried)."""
    tried = 0
    for x in cases:
        tried += 1
        if not claim(x):
            return x, tried
    return None, tried


def run_hunter(claims, limit):
    """Name -> (first counterexample or None, cases tried), trying start .. start + limit - 1."""
    return {c["name"]: hunt_count(c["claim"], range(c["start"], c["start"] + limit)) for c in claims}


def broken(results):
    """Sorted names of refuted claims."""
    return sorted(name for name, (ce, _) in results.items() if ce is not None)


def survivors(results):
    """Sorted names of claims with no counterexample found."""
    return sorted(name for name, (ce, _) in results.items() if ce is None)
