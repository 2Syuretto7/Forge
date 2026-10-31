import numpy as np
import sub

MU, L = 1.0, 100.0
ALPHA = 4 / (np.sqrt(L) + np.sqrt(MU)) ** 2
BETA = ((np.sqrt(L) - 1) / (np.sqrt(L) + 1)) ** 2


def test_optimal_momentum():
    b = sub.best_beta(ALPHA, MU, L, np.linspace(0.3, 0.95, 131))
    assert abs(b - BETA) < 0.006, (b, BETA)
    assert abs(sub.worst_radius(ALPHA, BETA, MU, L) - 9 / 11) < 1e-3


def test_equal_contraction():
    radii = [sub.spectral_radius(sub.momentum_matrix(lam, ALPHA, BETA)) for lam in np.linspace(1.5, 99, 20)]
    assert np.allclose(radii, np.sqrt(BETA), atol=1e-6)
    assert abs(sub.spectral_radius(sub.momentum_matrix(1.0, 0.01, 0.0)) - 0.99) < 1e-12
