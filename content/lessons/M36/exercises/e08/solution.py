import numpy as np


def policy(theta):
    """Row-wise softmax of the logits."""
    e = np.exp(theta - theta.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def _values(P, R, theta, gamma):
    pi = policy(theta)
    Ppi = np.einsum("sa,ast->st", pi, P)
    V = np.linalg.solve(np.eye(len(pi)) - gamma * Ppi, np.sum(pi * R, axis=1))
    Q = R + gamma * np.einsum("ast,t->sa", P, V)
    return pi, Ppi, V, Q


def objective(P, R, theta, rho0, gamma):
    """Expected discounted return from the start distribution."""
    _, _, V, _ = _values(P, R, theta, gamma)
    return float(rho0 @ V)


def policy_gradient(P, R, theta, rho0, gamma):
    """Exact policy gradient for a tabular softmax policy."""
    pi, Ppi, V, Q = _values(P, R, theta, gamma)
    d = np.linalg.solve((np.eye(len(pi)) - gamma * Ppi).T, rho0)
    return d[:, None] * pi * (Q - V[:, None])
