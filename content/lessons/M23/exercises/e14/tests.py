import numpy as np
import sub

BAD = np.array([[1.0, 0.9, 0.9], [0.9, 1.0, 0.0], [0.9, 0.0, 1.0]])


def factorable(M):
    try:
        L = np.linalg.cholesky(M)
    except np.linalg.LinAlgError:
        return False
    return bool(np.all(np.isfinite(L)) and np.all(np.diag(L) > 0))


def test_bad_matrix():
    assert not sub.is_psd(BAD)
    a = sub.negative_variance_direction(BAD)
    assert abs(np.linalg.norm(a) - 1) < 1e-12 and a @ BAD @ a < -0.2
    assert not factorable(BAD)


def test_repair():
    F = sub.nearest_correlation(BAD)
    assert sub.is_psd(F) and np.allclose(np.diag(F), 1) and np.allclose(F, F.T)
    assert factorable(F)
    assert np.max(np.abs(F - BAD)) < 0.4
    G = np.array([[1.0, 0.3], [0.3, 1.0]])
    assert np.allclose(sub.nearest_correlation(G), G, atol=1e-9)
