import numpy as np
import sub

rng = np.random.default_rng(0)


def test_trap():
    q = rng.normal(size=10)
    T = sub.make_trap(q, 3.0)
    assert abs(np.linalg.norm(T[1]) - 3) < 1e-12
    c = T[1] @ q / (3 * np.linalg.norm(q))
    assert abs(c - 0.5) < 1e-12
    assert sub.rank_by_dot(q, T) == [1, 0]
    assert sub.rank_by_cosine(q, T) == [0, 1]


def test_length_bias():
    q = rng.normal(size=20)
    X = rng.normal(size=(500, 20)) * rng.uniform(0.1, 10, size=(500, 1)) + 0.3 * q
    assert sub.length_bias(q, X) > 0.2
