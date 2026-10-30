import numpy as np
import sub

X, TRUE = sub.make_offset_cloud()
MEAN_DIR = X.mean(axis=0) / np.linalg.norm(X.mean(axis=0))


def test_uncentred_points_at_mean():
    u = sub.first_direction(X, centre=False)
    assert sub.alignment(u, MEAN_DIR) > 0.99
    assert sub.alignment(u, TRUE) < 0.9


def test_centred_finds_structure():
    u = sub.first_direction(X, centre=True)
    assert sub.alignment(u, TRUE) > 0.99
    assert sub.explained_first(X, False) > 0.95
    assert sub.explained_first(X, True) > 0.8
