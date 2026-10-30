import numpy as np
import sub

rng = np.random.default_rng(0)
X = rng.normal(size=(10000, 32))
Q = rng.normal(size=(50, 32))


def test_batch_matches_single_queries():
    index = sub.build_index(X)
    R = sub.batch_search(index, Q, 5)
    assert R.shape == (50, 5)
    for i in range(0, 50, 7):
        s = (X / np.linalg.norm(X, axis=1, keepdims=True)) @ (Q[i] / np.linalg.norm(Q[i]))
        assert list(R[i]) == list(np.argsort(-s)[:5])


def test_flops():
    assert sub.flops_per_query(100000, 32) == 6400000
