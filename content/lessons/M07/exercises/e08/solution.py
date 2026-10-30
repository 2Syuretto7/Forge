import math


def exp_series(z, terms=40):
    """Sum of z**k / k! for complex z."""
    total, term = 0j, 1 + 0j
    for k in range(terms):
        if k > 0:
            term *= z / k
        total += term
    return total


def euler_gap(theta):
    """|e^(i theta) - (cos theta + i sin theta)| with the series."""
    return abs(exp_series(1j * theta) - complex(math.cos(theta), math.sin(theta)))


def real_and_imaginary_terms(theta, terms=20):
    """Real and imaginary parts of the series terms of e^(i theta)."""
    out, term = [], 1 + 0j
    for k in range(terms):
        if k > 0:
            term *= 1j * theta / k
        out.append(term)
    return [t.real for t in out], [t.imag for t in out]
