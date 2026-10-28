import numpy as np
import sub


def test_norm_and_clip():
    g = [np.array([3.0, 0.0]), np.array([[4.0]])]
    assert sub.global_norm(g) == 5.0
    clipped, norm = sub.clip_by_global_norm(g, 1.0)
    assert norm == 5.0 and abs(sub.global_norm(clipped) - 1.0) < 1e-12
    assert np.allclose(clipped[0], [0.6, 0.0]) and np.allclose(clipped[1], [[0.8]])


def test_small_gradients_untouched():
    g = [np.array([0.1, 0.2])]
    clipped, norm = sub.clip_by_global_norm(g, 1.0)
    assert np.array_equal(clipped[0], g[0]) and abs(norm - np.sqrt(0.05)) < 1e-12
    assert np.array_equal(sub.clip_by_global_norm([np.zeros(3)], 1.0)[0][0], np.zeros(3))
