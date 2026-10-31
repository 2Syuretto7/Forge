import numpy as np
import sub

S = np.array([[2.0, 1.0], [1.0, 2.0]])
MU = np.array([1.0, -1.0])


def test_axes():
    w, V = sub.ellipse_axes(S)
    assert np.allclose(w, [3, 1]) and np.allclose(np.abs(V[:, 0]), [2**-0.5, 2**-0.5])
    assert np.allclose(S @ V, V * w)


def test_fractions_inside():
    rng = np.random.default_rng(4)
    X = MU + rng.standard_normal((200000, 2)) @ np.linalg.cholesky(S).T
    r = sub.mahalanobis(X, MU, S)
    for k in (1, 2, 3):
        assert abs(np.mean(r <= k) - sub.prob_inside(k)) < 0.004
    assert abs(sub.prob_inside(1) - 0.3935) < 1e-4


def test_points_lie_on_the_contour():
    P = sub.ellipse_points(MU, S, 2.0, 64)
    assert P.shape == (64, 2)
    assert np.allclose(sub.mahalanobis(P, MU, S), 2.0)
