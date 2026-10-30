import numpy as np
import sub

LINKS = [(0, 1), (0, 2), (1, 2), (2, 0), (3, 2), (4, 2), (4, 0)]


def test_matrix():
    G = sub.google_matrix(LINKS, 6)
    assert np.allclose(G.sum(axis=0), 1)
    assert np.allclose(G[:, 5], 1 / 6)
    assert np.isclose(G[1, 0], 0.85 / 2 + 0.15 / 6)


def test_rank():
    p = sub.pagerank(LINKS, 6)
    G = sub.google_matrix(LINKS, 6)
    assert np.isclose(p.sum(), 1) and np.allclose(G @ p, p)
    assert np.argmax(p) == 2
    lam, V = np.linalg.eig(G)
    v = np.real(V[:, np.argmax(np.real(lam))])
    assert np.allclose(p, v / v.sum(), atol=1e-9)
