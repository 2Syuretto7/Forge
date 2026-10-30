import numpy as np
import sub


def test_graph():
    src, dst = sub.make_graph(1000, k=5)
    assert src.size == dst.size == 950 * 5
    assert not np.any(src % 20 == 0) and dst.max() < 1000


def test_matches_dense():
    n = 200
    src, dst = sub.make_graph(n, k=4, seed=2)
    x, res = sub.pagerank_sparse(src, dst, n)
    out = np.bincount(src, minlength=n).astype(float)
    S = np.zeros((n, n))
    np.add.at(S, (dst, src), 1 / out[src])
    S[:, out == 0] = 1 / n
    G = 0.85 * S + 0.15 / n
    assert np.allclose(G @ x, x, atol=1e-9) and np.isclose(x.sum(), 1)
    assert res[-1] < 1e-10


def test_large():
    n = 20000
    src, dst = sub.make_graph(n)
    x, res = sub.pagerank_sparse(src, dst, n)
    assert np.isclose(x.sum(), 1) and res[-1] < 1e-10 and len(res) < 120
    assert np.argmax(x) < 50
