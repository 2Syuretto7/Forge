import numpy as np
import sub


def test_lemma_holds():
    rng = np.random.default_rng(0)
    X = rng.standard_normal((200, 1000)) * np.linspace(0.5, 2, 1000)
    k = sub.jl_dim(200, 0.3)
    assert k == 589
    Y = X @ sub.jl_matrix(1000, k, rng)
    assert sub.max_sq_distortion(X, Y) < 0.3


def test_distances():
    X = np.array([[0.0, 0.0], [3.0, 4.0], [1.0, 0.0]])
    D = sub.pairwise_sq_dists(X)
    assert np.allclose(D, [[0, 25, 1], [25, 0, 20], [1, 20, 0]])
    assert sub.max_sq_distortion(X, 2 * X) == 3.0
