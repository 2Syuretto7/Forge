import math


def frequencies(d, base=10000):
    """The d/2 rotation speeds base**(-2j/d)."""
    return [base ** (-2 * j / d) for j in range(d // 2)]


def rope(x, m, base=10000):
    """x with each pair (x[2j], x[2j+1]) turned by m * omega_j."""
    out = []
    for j, w in enumerate(frequencies(len(x), base)):
        a, b = x[2 * j], x[2 * j + 1]
        c, s = math.cos(m * w), math.sin(m * w)
        out += [a * c - b * s, a * s + b * c]
    return out


def dot(u, v):
    """Sum of u_i v_i."""
    return sum(a * b for a, b in zip(u, v))


def score(q, k, m, n):
    """Dot product of q encoded at m and k encoded at n."""
    return dot(rope(q, m), rope(k, n))
