import numpy as np
import sub

rng = np.random.default_rng(4)


def test_grad_matches_central_differences():
    for _ in range(10):
        z, c = rng.normal(size=6) * 3, int(rng.integers(6))
        g = sub.cross_entropy_grad(z, c)
        num = np.array([(sub.cross_entropy(z + 1e-6 * e, c) - sub.cross_entropy(z - 1e-6 * e, c)) / 2e-6 for e in np.eye(6)])
        assert np.allclose(g, num, atol=1e-8)
        assert np.allclose(sub.chain_check(z, c), g, atol=1e-12)
        assert abs(g.sum()) < 1e-12


def test_huge_logits():
    z = np.array([1000.0, 1001.0, 999.0])
    assert np.isfinite(sub.cross_entropy(z, 0))
    assert np.allclose(sub.cross_entropy_grad(z, 1), sub.chain_check(z, 1))
