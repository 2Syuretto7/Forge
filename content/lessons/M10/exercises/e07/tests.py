import numpy as np
import sub

rng = np.random.default_rng(0)


def test_square():
    sq = np.array([[0.0, 0], [1, 0], [1, 1], [0, 1]])
    assert sub.polygon_area(sq) == 1
    assert sub.polygon_area(sq[::-1]) == -1
    assert np.isclose(sub.area_ratio(np.array([[2.0, 1], [0, 1]]), sq), 2)


def test_invariant_area_scales_by_det():
    for _ in range(200):
        k = int(rng.integers(3, 12))
        ang = np.sort(rng.uniform(0, 2 * np.pi, size=k))
        r = rng.uniform(0.5, 2, size=k)
        P = np.column_stack([r * np.cos(ang), r * np.sin(ang)])
        M = rng.normal(size=(2, 2))
        assert np.isclose(sub.area_ratio(M, P), np.linalg.det(M))
