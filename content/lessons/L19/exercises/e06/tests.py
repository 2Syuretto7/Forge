import numpy as np
import sub


def test_interference_falls_with_dimension():
    vals = [sub.mean_interference(sub.random_unit_vectors(200, d)) for d in (16, 64, 256)]
    for v, d in zip(vals, (16, 64, 256)):
        assert abs(v * d - 1) < 0.15
    assert sub.max_interference(sub.random_unit_vectors(200, 256)) < 0.35
    V = sub.random_unit_vectors(5, 3)
    assert np.allclose(np.linalg.norm(V, axis=1), 1)
