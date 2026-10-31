import numpy as np
import sub

X = sub.make_embeddings()


def test_compression():
    k = sub.smallest_k(X, [128, 256, 512, 768, 1024])
    assert k is not None and k <= 1024
    R = np.random.default_rng(0).standard_normal((2048, k)) / np.sqrt(k)
    assert sub.max_distortion(X, sub.matmul_blocked(X, R)) <= 0.1
    assert sub.jl_bound_k(100, 0.19) > k
    Y = sub.jl_project(X, 64)
    R64 = np.random.default_rng(0).standard_normal((2048, 64)) / 8
    assert Y.shape == (100, 64) and np.allclose(Y, X @ R64)
    assert sub.max_distortion(X, Y) > 0.1
    assert len(sub.pairwise_dists(X)) == 4950


def test_checks():
    v = sub.attention_check()
    assert set(v) == {16, 256, 1024} and all(abs(x - 1) < 0.1 for x in v.values())
    assert 0.2 < sub.init_check() < 5


def test_report():
    text = sub.REPORT.lower()
    assert len(sub.REPORT.split()) >= 120
    for w in ("johnson-lindenstrauss", "distortion", "square root", "initialization"):
        assert w in text, w
