import numpy as np
import sub

X, NAMES = sub.make_embeddings(0)
mean, comps, ratios = sub.fit_pca(X)


def test_shapes_and_ratios():
    assert mean.shape == (48,) and comps.shape == (48, 48) and ratios.shape == (48,)
    assert abs(ratios.sum() - 1) < 1e-10
    assert np.all(np.diff(ratios) <= 1e-15), "ratios must be descending"


def test_components_orthonormal_and_signed():
    assert np.allclose(comps @ comps.T, np.eye(48), atol=1e-9)
    for row in comps[:6]:
        assert row[np.argmax(np.abs(row))] > 0


def test_k_for_95_percent():
    k = sub.k_for_variance(ratios, 0.95)
    c = np.cumsum(ratios)
    assert c[k - 1] >= 0.95 and c[k - 2] < 0.95, f"k = {k} is not the smallest"
    assert k == 4
    assert sub.k_for_variance(np.array([0.5, 0.3, 0.2]), 0.8) == 2


def test_reconstruction_error_identity():
    for k in [1, 3, 4]:
        Xh = sub.reconstruct(X, mean, comps, k)
        Xc = X - X.mean(axis=0)
        rel = np.sum((X - Xh) ** 2) / np.sum(Xc ** 2)
        assert abs(rel - (1 - ratios[:k].sum())) < 1e-9


def test_top_groups_are_the_strong_factors():
    assert list(sub.top_groups(comps, NAMES, 3)) == ["science", "finance", "music"]


def test_report_interprets_the_components():
    words = sub.REPORT.split()
    assert len(words) >= 80, f"report has {len(words)} words; write at least 80"
    text = sub.REPORT.lower()
    for g in ["science", "finance", "music"]:
        assert g in text, f"the report should say which group component(s) measure: missing {g}"
