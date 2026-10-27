import numpy as np
import sub

rng = np.random.default_rng(11)
n, d = 300, 6
Z = rng.normal(size=(n, 2)) * np.array([5.0, 2.0])
W = np.linalg.qr(rng.normal(size=(d, 2)))[0].T
X = Z @ W + 0.1 * rng.normal(size=(n, d)) + 3.0


def test_shapes():
    out = sub.pca(X, 3)
    assert out["mean"].shape == (6,)
    assert out["components"].shape == (3, 6)
    assert out["explained_variance"].shape == (3,)
    assert out["scores"].shape == (300, 3)


def test_variance_matches_covariance_eigenvalues():
    out = sub.pca(X, 3)
    C = np.cov(X, rowvar=False)
    w = np.sort(np.linalg.eigvalsh(C))[::-1]
    assert np.allclose(out["explained_variance"], w[:3], rtol=1e-10)


def test_components_orthonormal_with_sign_convention():
    c = sub.pca(X, 4)["components"]
    assert np.allclose(c @ c.T, np.eye(4), atol=1e-10)
    for row in c:
        assert row[np.argmax(np.abs(row))] > 0


def test_ratios_and_scores():
    out = sub.pca(X, 6)
    assert abs(out["explained_variance_ratio"].sum() - 1) < 1e-12
    assert out["explained_variance_ratio"][:2].sum() > 0.99, "two factors dominate this data"
    Xc = X - X.mean(axis=0)
    assert np.allclose(out["scores"], Xc @ out["components"].T)


def test_scores_variance_equals_explained_variance():
    out = sub.pca(X, 2)
    assert np.allclose(out["scores"].var(axis=0, ddof=1), out["explained_variance"], rtol=1e-10)
