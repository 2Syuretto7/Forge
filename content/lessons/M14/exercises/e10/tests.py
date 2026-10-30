import numpy as np
import sub

X = sub.make_embeddings(2000, 128)
S_ALL = np.linalg.svd(X - X.mean(axis=0), compute_uv=False)


def test_top_k_matches_svd():
    s, Vt = sub.top_k_svd(X, 10)
    assert s.shape == (10,) and Vt.shape == (10, 128)
    assert np.allclose(s, S_ALL[:10], rtol=1e-8)
    assert np.allclose(Vt @ Vt.T, np.eye(10), atol=1e-8)


def test_eckart_young_and_rank():
    _, Vt = sub.top_k_svd(X, 20)
    e = sub.explained(S_ALL)
    assert np.isclose(sub.recon_error(X, Vt), np.sqrt(1 - e[19]), rtol=1e-6)
    k = sub.rank_for(S_ALL, 0.95)
    assert e[k - 1] >= 0.95 and e[k - 2] < 0.95
    assert k > 60, "a power-law spectrum needs many directions"
