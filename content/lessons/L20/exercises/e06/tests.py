import numpy as np
import sub

rng = np.random.default_rng(4)
U, _ = np.linalg.qr(rng.normal(size=(16, 16)))
V, _ = np.linalg.qr(rng.normal(size=(16, 16)))
target = (U[:, :4] * np.array([1.0, 0.7, 0.5, 0.3])) @ V[:, :4].T


def test_reaches_the_svd_optimum():
    S = np.linalg.svd(target, compute_uv=False)
    for r in [1, 2, 4]:
        A, B, loss = sub.fit_lora(target, r, alpha=r)
        assert A.shape == (r, 16) and B.shape == (16, r)
        assert abs(loss - 0.5 * np.sum(S[r:] ** 2)) < 2e-3


def test_starts_at_the_base_model():
    A, B, _ = sub.fit_lora(target, 2, alpha=2, steps=0)
    assert np.all(B == 0)
