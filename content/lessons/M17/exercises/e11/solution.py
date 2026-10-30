import numpy as np


def richardson(t_h, t_h2, p):
    """Cancel the h^p error term."""
    return (2 ** p * t_h2 - t_h) / (2 ** p - 1)


def romberg(f, a, b, levels):
    """Romberg integration."""
    R = []
    for i in range(levels):
        n = 2 ** i
        x = np.linspace(a, b, n + 1)
        y = f(x)
        row = [(b - a) / n * (y.sum() - (y[0] + y[-1]) / 2)]
        for k in range(1, i + 1):
            row.append(richardson(R[i - 1][k - 1], row[k - 1], 2 * k))
        R.append(row)
    return float(R[-1][-1])
