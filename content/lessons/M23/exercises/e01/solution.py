import numpy as np


def marginal(joint, axis):
    """Distribution of X (axis=0) or of Y (axis=1)."""
    joint = np.asarray(joint, dtype=float)
    return joint.sum(axis=1) if axis == 0 else joint.sum(axis=0)


def conditional_y_given_x(joint):
    """Table of P(Y = j | X = i)."""
    joint = np.asarray(joint, dtype=float)
    px = joint.sum(axis=1)
    if np.any(px == 0):
        raise ValueError("conditioning on a value of X with probability 0")
    return joint / px[:, None]


def is_independent(joint, tol=1e-12):
    """Whether the joint table factorizes into its marginals."""
    joint = np.asarray(joint, dtype=float)
    return bool(np.max(np.abs(joint - np.outer(marginal(joint, 0), marginal(joint, 1)))) <= tol)


def from_conditional(px, cond):
    """Joint table from P(X) and P(Y | X)."""
    return np.asarray(px, dtype=float)[:, None] * np.asarray(cond, dtype=float)
