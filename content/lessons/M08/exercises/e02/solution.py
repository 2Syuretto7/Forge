def factorial(n):
    """n! exactly."""
    out = 1
    for k in range(2, n + 1):
        out *= k
    return out


def arrangements(n, k):
    """n! / (n - k)! as a product of k factors."""
    out = 1
    for i in range(k):
        out *= n - i
    return out


def all_permutations(items):
    """Every ordering of items, each a list."""
    if not items:
        return [[]]
    out = []
    for i, first in enumerate(items):
        for rest in all_permutations(items[:i] + items[i + 1:]):
            out.append([first] + rest)
    return out
