import numpy as np


def rates(A):
    """Speed limits of gradient descent on a quadratic with symmetric positive definite Hessian A."""
    raise NotImplementedError


def contraction(A, lr):
    """Worst-case factor by which one step multiplies the error: max_i |1 - lr * lambda_i|."""
    raise NotImplementedError


def steps_needed(A, eps):
    """Steps at the optimal fixed rate until the worst-case error shrinks by eps."""
    raise NotImplementedError
