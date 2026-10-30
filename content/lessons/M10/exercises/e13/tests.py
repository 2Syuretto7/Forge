import numpy as np
import sub

SQ = np.array([[0.0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])


def r(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def test_pipeline_order():
    T = np.array([[1.0, 0, 5], [0, 1, 0], [0, 0, 1]])
    M = sub.pipeline_matrix([T, r(np.pi / 2)])
    assert np.allclose(M @ [0, 0, 1], [0, 5, 1])


def test_commutes():
    assert sub.commutes(r(0.3), r(1.1))
    assert sub.commutes(np.diag([2.0, 2, 1]), r(0.7))
    assert not sub.commutes(np.diag([2.0, 1, 1]), r(0.7))


def test_logo_lands_rotated_at_target():
    M = sub.pipeline_matrix(sub.place_logo())
    out = SQ @ M.T
    assert np.allclose(out[:, :2].mean(axis=0), [3, 2])
    edge = out[1, :2] - out[0, :2]
    assert np.isclose(np.degrees(np.arctan2(edge[1], edge[0])), 45)
    assert np.isclose(np.linalg.norm(edge), 1)
