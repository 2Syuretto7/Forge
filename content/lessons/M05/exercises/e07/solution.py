def count_pairs(n):
    """Iterations of for i in range(n): for j in range(i)."""
    c = 0
    for i in range(n):
        for _ in range(i):
            c += 1
    return c


def count_triples(n):
    """Iterations of three nested loops over k < j < i < n."""
    c = 0
    for i in range(n):
        for j in range(i):
            for _ in range(j):
                c += 1
    return c


def count_halvings(n):
    """Iterations of while m > 0: m //= 2, from m = n."""
    c, m = 0, n
    while m > 0:
        m //= 2
        c += 1
    return c


def formulas(n):
    """(n choose 2, n choose 3, number of binary digits of n)."""
    return n * (n - 1) // 2, n * (n - 1) * (n - 2) // 6, n.bit_length()
