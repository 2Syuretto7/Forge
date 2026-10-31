import numpy as np
import sub

TEST = sub.make_embeddings(3000, seed=99)


def test_fit():
    X = sub.make_embeddings(500, seed=1)
    m, S = sub.fit(X)
    assert m.shape == (256,) and S.shape == (256, 256)
    assert np.allclose(S, np.cov(X, rowvar=False, bias=True))
    assert np.allclose(np.trace(sub.shrink(S, 0.3)), np.trace(S))


def test_more_data_and_shrinkage():
    small = sub.make_embeddings(300, seed=1)
    big = sub.make_embeddings(10000, seed=2)
    raw_small = sub.heldout_loglik(small, TEST)
    raw_big = sub.heldout_loglik(big, TEST)
    shrunk_small = sub.heldout_loglik(small, TEST, 0.3)
    assert raw_big > raw_small + 300, (raw_small, raw_big)
    assert shrunk_small > raw_small + 300
    assert raw_big > shrunk_small
