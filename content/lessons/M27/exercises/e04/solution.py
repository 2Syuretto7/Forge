import numpy as np


def marginals(P):
    P = np.asarray(P, dtype=float)
    return P.sum(axis=1), P.sum(axis=0)


def conditional_entropy(P):
    P = np.asarray(P, dtype=float)
    px, _ = marginals(P)
    m = P > 0
    cond = P / px[:, None]
    return float(-np.sum(P[m] * np.log(cond[m])))


def mutual_information(P):
    P = np.asarray(P, dtype=float)
    px, py = marginals(P)
    m = P > 0
    return float(np.sum(P[m] * np.log(P[m] / np.outer(px, py)[m])))
