import numpy as np


def integrate_polar(g, R, n=400):
    """Midpoint rule in polar coordinates, with the Jacobian r."""
    dr, dt = R / n, 2 * np.pi / n
    r = dr * (np.arange(n) + 0.5)
    t = dt * (np.arange(n) + 0.5)
    Rr, T = np.meshgrid(r, t, indexing="ij")
    return float(np.sum(g(Rr * np.cos(T), Rr * np.sin(T)) * Rr) * dr * dt)
