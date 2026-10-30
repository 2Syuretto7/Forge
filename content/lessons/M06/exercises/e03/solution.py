def exp_series(x, terms=30):
    """Sum of x**k / k! for k = 0 .. terms - 1."""
    total, term = 0.0, 1.0
    for k in range(terms):
        if k > 0:
            term *= x / k
        total += term
    return total


def exp(x):
    """e**x by argument reduction and squaring."""
    k = 0
    while abs(x) / 2 ** k > 1:
        k += 1
    y = exp_series(x / 2 ** k)
    for _ in range(k):
        y = y * y
    return y
