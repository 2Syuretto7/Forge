import numpy as np
import sub


def test_primitives():
    assert np.allclose(sub.rot(90) @ [1, 0], [0, 1])
    assert np.allclose(sub.shear_x(2) @ [1, 1], [3, 1])
    assert np.allclose(sub.swap() @ [1, 2], [2, 1])
    assert np.allclose(sub.build([sub.scale(2, 1), sub.rot(90)]), sub.rot(90) @ sub.scale(2, 1))


def test_fit_matrix():
    M = np.array([[0.3, -1.2], [0.7, 2.0]])
    assert np.allclose(sub.fit_matrix(sub.F, sub.F @ M.T), M)


def test_all_targets():
    rep = sub.report()
    assert len(rep) == 8
    for i, (err, diff, det) in enumerate(rep):
        assert err < 1e-9, f"target {i + 1} ({sub.TARGETS[i][0]}): points off by {err:.3g}"
        assert diff < 1e-9, f"target {i + 1}: differs from the fitted matrix by {diff:.3g}"


def test_determinants_tell_the_story():
    dets = [d for _, _, d in sub.report()]
    assert np.allclose(dets, [1, -1, 1, 1, 2, 2, -1, 1])
