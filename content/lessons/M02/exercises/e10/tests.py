import numpy as np
import sub

rng = np.random.default_rng(0)
A = rng.uniform(-1, 1, size=(10000, 2, 2))
R = rng.uniform(-1, 1, size=(10000, 2))


def test_determinants():
    assert np.allclose(sub.determinants(A), np.linalg.det(A), atol=1e-12)


def test_solve_many_matches_numpy():
    X = sub.solve_many(A, R)
    assert X.shape == (10000, 2)
    good = np.abs(np.linalg.det(A)) > 1e-3
    assert np.allclose(X[good], np.linalg.solve(A[good], R[good][..., None])[..., 0], rtol=1e-8, atol=1e-10)


def test_invariant_solutions_satisfy_the_systems():
    X = sub.solve_many(A, R)
    good = np.abs(np.linalg.det(A)) > 1e-3
    res = np.einsum("nij,nj->ni", A, X) - R
    assert np.max(np.abs(res[good])) < 1e-9
