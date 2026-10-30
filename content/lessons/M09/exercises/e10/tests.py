import numpy as np
import sub


def test_agree():
    X = sub.make_database(5000, 32)
    q = sub.make_database(1, 32, seed=3)[0]
    assert sub.search_loop(q, X, 5) == sub.search_vectorized(q, X, 5)
    assert X.dtype == np.float32 and X.shape == (5000, 32)


def test_speedup():
    s = sub.speedup(20000, 32)
    assert s > 10, f"vectorized search was only {s:.1f} times faster"
