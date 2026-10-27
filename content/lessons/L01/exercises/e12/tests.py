import numpy as np
import sub

rng = np.random.default_rng(12)
yy, xx = np.mgrid[0:64, 0:48] / 48.0
IMG = (np.sin(6 * xx) * np.cos(4 * yy) + np.exp(-((xx - 0.5) ** 2 + (yy - 0.7) ** 2) * 20)
       + 0.3 * (xx > 0.6) + 0.02 * rng.normal(size=(64, 48)))
S = np.linalg.svd(IMG, compute_uv=False)


def test_rank_and_shape():
    A5 = sub.rank_k_approx(IMG, 5)
    assert A5.shape == IMG.shape
    assert np.linalg.matrix_rank(A5) == 5


def test_error_formula_matches_direct_error():
    for k in [1, 3, 10]:
        direct = np.linalg.norm(IMG - sub.rank_k_approx(IMG, k))
        assert abs(sub.eckart_young_error(S, k) - direct) < 1e-9


def test_no_random_rank_k_matrix_does_better():
    k = 4
    best = sub.eckart_young_error(S, k)
    for _ in range(20):
        Q = np.linalg.qr(rng.normal(size=(64, k)))[0]
        competitor = Q @ (Q.T @ IMG)  # best fit within a random k-dim column space
        assert np.linalg.norm(IMG - competitor) >= best - 1e-12


def test_compression_and_smallest_k():
    assert abs(sub.compression_ratio(64, 48, 4) - 3072 / 452) < 1e-12
    k = sub.smallest_k(IMG, 0.05)
    assert sub.eckart_young_error(S, k) / np.linalg.norm(IMG) <= 0.05
    assert k == 0 or sub.eckart_young_error(S, k - 1) / np.linalg.norm(IMG) > 0.05
    assert sub.smallest_k(IMG, 1.0) == 0
