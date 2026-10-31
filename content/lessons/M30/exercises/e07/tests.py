import numpy as np
import sub

rng = np.random.default_rng(7)
X = rng.normal(size=(300, 2))
Y = np.sign(X @ np.array([1.0, 1.0]) + 0.4 * rng.normal(size=300))


def test_categories_match_margins():
    a, w = sub.coordinate_ascent(X, Y, 1.0, 200, np.random.default_rng(1))
    assert sub.slackness_violations(a, w, X, Y, 1.0) == 0
    cat = sub.categories(a, 1.0)
    assert np.sum(cat == 0) > 150 and np.sum(cat == 1) >= 1
    assert list(sub.categories(np.array([0.0, 0.5, 1.0]), 1.0)) == [0, 1, 2]


def test_only_support_vectors_matter():
    a, w = sub.coordinate_ascent(X, Y, 1.0, 200, np.random.default_rng(2))
    w2 = sub.refit_on_support(X, Y, a, 1.0, 400, np.random.default_rng(3))
    assert np.allclose(w, w2, atol=1e-4)
