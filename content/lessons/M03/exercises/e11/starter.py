RESULTS = {
    "every prime is odd": (2, 1),
    "every odd number above 1 is prime": (9, 7),
    "n^2 + n + 41 is prime": (40, 41),
    "n^2 - n + 41 is prime": (41, 42),
    "2^n - 1 is prime for prime n": (11, 10),
    "2^(2^n) + 1 is prime": (5, 6),
    "n! + 1 is prime": (4, 4),
    "2^n > n^2": (2, 2),
    "n^2 >= 2n": (1, 1),
    "n < 100": (None, 60),
    "6n + 1 or 6n - 1 is prime": (20, 20),
    "n^2 + 1 is prime for even n": (0, 1),
    "3n + 1 is not a square": (0, 1),
    "n^2 + n + 17 is prime": (16, 17),
    "n divides 2^n - 2 only for prime n": (None, 60),
    "n^2 + n + 1 is prime": (4, 4),
    "10n + 1 is prime": (2, 2),
    "n and n + 2 are never both prime": (3, 2),
    "n^3 + 2 is prime for odd n": (7, 7),
    "4n + 3 is prime": (3, 4),
    "every number is a sum of at most three squares": (7, 8),
    "n^2 + 2 is not divisible by 3": (1, 2),
    "n^5 - n is divisible by 10 only for even n": (1, 2),
    "between n and 2n there are at least two primes": (1, 1),
    "11...1 with n ones is not divisible by 11": (2, 2),
    "n^3 - n is divisible by 6": (None, 60),
    "1 + 3 + ... + (2n - 1) = n^2": (None, 60),
    "n^2 leaves remainder 0 or 1 mod 4": (None, 60),
    "n(n + 1)(n + 2) is divisible by 6": (None, 60),
    "1 + 2 + ... + n = n(n + 1)/2": (None, 60),
    "n^2 + 1 is not divisible by 3": (None, 60),
    "n^5 - n is divisible by 5": (None, 60),
    "2^n >= n + 1": (None, 60),
    "n! >= 2^(n - 1)": (None, 60),
    "there is a prime between n and 2n": (None, 60),
    "every number above 1 has a prime divisor": (None, 60),
    "the sum of the digits of 9n is divisible by 9": (None, 60),
    "n^2 - n is even": (None, 60),
    "every number is a sum of four squares": (None, 60),
    "gcd(n, n + 1) = 1": (None, 60),
    "3^n - 1 is even": (None, 60),
    "7^n - 1 is divisible by 6": (None, 60),
    "n^3 + 2n is divisible by 3": (None, 60),
    "the last digit of n^4 is 0, 1, 5 or 6": (None, 60),
    "1^3 + ... + n^3 = (1 + ... + n)^2": (None, 60),
    "fib(n) and fib(n + 1) share no factor": (None, 60),
    "n^2 + n is even": (None, 60),
    "a prime above 3 leaves remainder 1 or 5 mod 6": (None, 60),
    "8 divides n^2 - 1 for odd n": (None, 60),
    "the product of n consecutive numbers is divisible by n!": (None, 60),
}


def survival_times(results):
    """Sorted tries of the refuted claims."""
    raise NotImplementedError


def median(xs):
    """Middle value of a sorted list."""
    raise NotImplementedError


def longest_survivor(results):
    """Name of the refuted claim with the most tries (alphabetical tie-break)."""
    raise NotImplementedError


def share_within(results, k):
    """Fraction of refuted claims that broke within k tries."""
    raise NotImplementedError
