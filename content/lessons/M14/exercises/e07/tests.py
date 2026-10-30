import numpy as np
import sub

rng = np.random.default_rng(10)
A = rng.normal(size=(5, 5))
P = np.array([[1.0, 1.0], [1.0, 1.0001]])


def test_cond_matches_numpy():
    assert abs(sub.cond2(A) / np.linalg.cond(A) - 1) < 1e-10
    assert abs(sub.cond2(P) - 40002.0) < 1.0


def test_amplification_never_exceeds_cond():
    k = sub.cond2(A)
    for _ in range(200):
        a = sub.amplification(A, rng.normal(size=5), 1e-6 * rng.normal(size=5))
        assert a <= k * (1 + 1e-8), f"amplification {a} exceeds kappa {k}"


def test_worst_case_attains_the_bound():
    b, db = sub.worst_case_pair(A)
    assert abs(np.linalg.norm(b) - 1) < 1e-12 and abs(np.linalg.norm(db) - 1) < 1e-12
    assert abs(sub.amplification(A, b, db) / sub.cond2(A) - 1) < 1e-8


def test_puzzle_matrix_amplifies_tens_of_thousands():
    b, db = sub.worst_case_pair(P)
    assert sub.amplification(P, b, db) > 39000
