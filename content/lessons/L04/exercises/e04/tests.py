import numpy as np
import sub

rng = np.random.default_rng(4)


def H(p):
    p = np.asarray(p).ravel()
    p = p[p > 0]
    return -np.sum(p * np.log(p))


def test_identities():
    P = rng.dirichlet(np.ones(12)).reshape(3, 4)
    px, py = sub.marginals(P)
    assert abs(sub.mutual_information(P) - (H(py) - sub.conditional_entropy(P))) < 1e-12
    assert abs(H(P) - (H(px) + sub.conditional_entropy(P))) < 1e-12
    assert sub.mutual_information(P) >= -1e-15


def test_independent_variables():
    P = np.outer([0.2, 0.8], [0.1, 0.6, 0.3])
    assert abs(sub.mutual_information(P)) < 1e-15


def test_copy_of_a_fair_coin():
    P = np.array([[0.5, 0.0], [0.0, 0.5]])
    assert abs(sub.mutual_information(P) - np.log(2)) < 1e-12
    assert abs(sub.conditional_entropy(P)) < 1e-15
