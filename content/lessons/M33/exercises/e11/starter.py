import numpy as np


def ridge_loss(w, X, y, lam):
    """Half squared error plus half lambda times the squared norm."""
    raise NotImplementedError


def grad_ridge_loss(w, X, y, lam):
    """Gradient of ridge_loss."""
    raise NotImplementedError


def ridge_cg(X, y, lam, tol=1e-10):
    """Matrix-free CG on the ridge normal equations: (w, products)."""
    raise NotImplementedError


def ridge_direct(X, y, lam):
    """Ridge solution from the formed normal equations."""
    raise NotImplementedError
