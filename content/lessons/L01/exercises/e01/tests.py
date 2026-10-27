import numpy as np
import sub

rng = np.random.default_rng(0)


def test_values_match_numpy():
    x, y = rng.normal(size=7), rng.normal(size=7)
    assert abs(sub.dot(x, y) - float(x @ y)) < 1e-12
    assert abs(sub.norm(x) - float(np.linalg.norm(x))) < 1e-12
    assert isinstance(sub.dot(x, y), float), "dot should return a Python float"


def test_known_angles():
    assert abs(sub.angle_degrees(np.array([1.0, 0]), np.array([0, 2.0])) - 90) < 1e-9
    assert abs(sub.angle_degrees(np.array([1.0, 1]), np.array([1.0, 0])) - 45) < 1e-9
    assert abs(sub.angle_degrees(np.array([3.0, 4]), np.array([-6.0, -8])) - 180) < 1e-6


def test_parallel_vectors_do_not_give_nan():
    x = np.array([0.1, 0.2, 0.3])
    a = sub.angle_degrees(x, 3 * x)
    assert np.isfinite(a) and abs(a) < 1e-5, f"got {a}"


def test_cauchy_schwarz_invariant():
    for _ in range(50):
        x, y = rng.normal(size=5), rng.normal(size=5)
        assert abs(sub.dot(x, y)) <= sub.norm(x) * sub.norm(y) + 1e-12
        assert -1 - 1e-12 <= sub.cosine_similarity(x, y) <= 1 + 1e-12


def test_cosine_is_scale_invariant():
    x, y = rng.normal(size=4), rng.normal(size=4)
    assert abs(sub.cosine_similarity(5 * x, 0.1 * y) - sub.cosine_similarity(x, y)) < 1e-12
