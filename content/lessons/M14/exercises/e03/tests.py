import numpy as np
import sub

rng = np.random.default_rng(3)


def test_example():
    s1, s2 = sub.singular_values_2x2(np.array([[3.0, 0], [4, 5]]))
    assert np.isclose(s1, np.sqrt(45)) and np.isclose(s2, np.sqrt(5))


def test_invariant_ellipse():
    for _ in range(100):
        A = rng.normal(size=(2, 2))
        s1, s2 = sub.singular_values_2x2(A)
        hi, lo = sub.circle_image_extremes(A)
        assert abs(hi - s1) < 1e-5 * s1 and abs(lo - s2) < 1e-5 * s1
        assert np.isclose(s1 * s2, sub.area_factor(A))
        assert np.allclose([s1, s2], np.linalg.svd(A, compute_uv=False))
