import numpy as np


def primal_objective(w, X, y, C):
    """Soft-margin SVM objective."""
    raise NotImplementedError


def margin_violations(w, X, y):
    """Points inside the margin or misclassified."""
    raise NotImplementedError


def subgradient(w, X, y, C):
    """A subgradient of the primal objective."""
    raise NotImplementedError


def subgradient_descent(X, y, C, iters):
    """Best iterate of the subgradient method with steps 1/(k+1)."""
    raise NotImplementedError
