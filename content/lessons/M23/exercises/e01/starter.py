import numpy as np


def marginal(joint, axis):
    """Distribution of X (axis=0) or of Y (axis=1)."""
    raise NotImplementedError


def conditional_y_given_x(joint):
    """Table of P(Y = j | X = i)."""
    raise NotImplementedError


def is_independent(joint, tol=1e-12):
    """Whether the joint table factorizes into its marginals."""
    raise NotImplementedError


def from_conditional(px, cond):
    """Joint table from P(X) and P(Y | X)."""
    raise NotImplementedError
