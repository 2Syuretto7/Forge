import numpy as np
import sub

rng = np.random.default_rng(3)


def test_factor():
    A = rng.normal(size=(30, 30))
    perm, L, U = sub.lu_fast(A)
    assert np.allclose(A[perm], L @ U)
    assert np.allclose(U, np.triu(U)) and np.all(np.abs(L) <= 1 + 1e-12)


def test_compare():
    r = sub.compare(150)
    assert set(r) == {"mine_s", "numpy_s", "mine_res", "numpy_res"}
    assert r["mine_res"] < 1e-13 and r["numpy_res"] < 1e-13
    assert r["mine_s"] > 0 and r["numpy_s"] > 0
