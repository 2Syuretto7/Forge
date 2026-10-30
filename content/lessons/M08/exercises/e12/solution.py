import math


def bits_needed(n, p):
    """Smallest b with C(n, 2) / 2**b <= p."""
    b = max(0, math.ceil(math.log2(math.comb(n, 2) / p)) - 1)
    while math.comb(n, 2) / 2 ** b > p:
        b += 1
    return b


def max_documents(bits, p):
    """Largest n with C(n, 2) / 2**bits <= p."""
    n = int(math.isqrt(int(2 * p * 2 ** bits))) + 2
    while n > 1 and math.comb(n, 2) / 2 ** bits > p:
        n -= 1
    return n
