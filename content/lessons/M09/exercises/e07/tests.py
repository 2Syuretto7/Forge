import numpy as np
import sub

rng = np.random.default_rng(1)
X = rng.normal(size=(500, 16))


def test_top_k():
    q = X[42] * 2.5
    t = sub.top_k(q, X, 3)
    assert t[0] == 42 and len(t) == 3
    s = (X @ q) / np.linalg.norm(X, axis=1)
    assert s[t[0]] >= s[t[1]] >= s[t[2]]


def test_euclidean_and_cosine_agree_on_unit_vectors():
    for _ in range(10):
        assert sub.same_order_when_normalized(rng.normal(size=16), X, 10)


def test_euclidean_can_disagree_without_normalizing():
    q = np.ones(16)
    Y = np.vstack([np.ones(16) * 10, np.ones(16) * 0.9 + 0.3 * rng.normal(size=16)])
    assert sub.top_k(q, Y, 1) == [0] and sub.top_k_euclidean(q, Y, 1) == [1]
