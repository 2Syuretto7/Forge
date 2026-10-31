import numpy as np


def momentum_matrix(lam, alpha, beta):
    """Iteration matrix of heavy ball along one eigenvector."""
    return np.array([[1 + beta - alpha * lam, -beta], [1.0, 0.0]])


def spectral_radius(M):
    """Largest eigenvalue modulus."""
    return float(np.max(np.abs(np.linalg.eigvals(M))))


def worst_radius(alpha, beta, mu, L, n=200):
    """Largest spectral radius over curvatures in [mu, L]."""
    return max(spectral_radius(momentum_matrix(lam, alpha, beta)) for lam in np.linspace(mu, L, n))


def best_beta(alpha, mu, L, betas):
    """Momentum with the smallest worst radius."""
    return min(betas, key=lambda b: worst_radius(alpha, b, mu, L))
