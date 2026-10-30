import numpy as np
import sub

SQ = np.array([[0.0, 0], [2, 0], [2, 2], [0, 2]])


def test_apply_and_compose():
    S = np.array([[2.0, 0], [0, 1]])
    R = np.array([[0.0, -1], [1, 0]])
    assert np.allclose(sub.apply(S, SQ), [[0, 0], [4, 0], [4, 2], [0, 2]])
    M = sub.compose(S, R)
    assert np.allclose(sub.apply(M, SQ), sub.apply(R, sub.apply(S, SQ)))
    assert not np.allclose(sub.compose(S, R), sub.compose(R, S))
    assert np.allclose(sub.compose(S, R, S), S @ R @ S)


def test_homogeneous():
    H = sub.to_h(SQ)
    assert H.shape == (4, 3)
    assert np.allclose(sub.from_h(sub.apply(sub.translate(1, -1), H)), SQ + [1, -1])


def test_rotate_about_centre():
    M = sub.rotate_about(np.pi / 2, (1.0, 1.0))
    out = sub.from_h(sub.apply(M, sub.to_h(SQ)))
    assert np.allclose(out.mean(axis=0), [1, 1])
    assert np.allclose(out, [[2, 0], [2, 2], [0, 2], [0, 0]])
