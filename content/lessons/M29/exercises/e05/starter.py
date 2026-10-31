import numpy as np


def momentum_matrix(lam, alpha, beta):
    """Iteration matrix of heavy ball along one eigenvector."""
    raise NotImplementedError


def spectral_radius(M):
    """Largest eigenvalue modulus."""
    raise NotImplementedError


def worst_radius(alpha, beta, mu, L, n=200):
    """Largest spectral radius over curvatures in [mu, L]."""
    raise NotImplementedError


def best_beta(alpha, mu, L, betas):
    """Momentum with the smallest worst radius."""
    raise NotImplementedError
