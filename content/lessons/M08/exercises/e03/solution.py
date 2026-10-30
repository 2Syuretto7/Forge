import math


def comb_factorial(n, k):
    """n! / (k! (n-k)!) exactly."""
    if k < 0 or k > n:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def comb_pascal(n, k):
    """From rows of Pascal's triangle."""
    if k < 0 or k > n:
        return 0
    row = [1]
    for _ in range(n):
        row = [1] + [row[i - 1] + row[i] for i in range(1, len(row))] + [1]
    return row[k]


def comb_multiplicative(n, k):
    """Product of (n - k + i) / i, exact at every step."""
    if k < 0 or k > n:
        return 0
    c = 1
    for i in range(1, k + 1):
        c = c * (n - k + i) // i
    return c
