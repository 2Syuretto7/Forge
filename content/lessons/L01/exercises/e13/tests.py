import numpy as np
import sub

rng = np.random.default_rng(13)
X = rng.uniform(-2, 2, size=(500, 2))
y = (np.sum(X ** 2, axis=1) < 1.6).astype(float)


def test_poly_features():
    F = sub.poly2(np.array([[2.0, 3.0]]))
    assert np.allclose(F, [[1, 2, 3, 4, 6, 9]])


def test_quadratic_features_separate_a_circle():
    lin_tr = np.column_stack([np.ones(400), X[:400]])
    lin_te = np.column_stack([np.ones(100), X[400:]])
    acc_lin = sub.fit_and_score(lin_tr, y[:400], lin_te, y[400:])
    acc_quad = sub.fit_and_score(sub.poly2(X[:400]), y[:400], sub.poly2(X[400:]), y[400:])
    assert acc_lin < 0.75, acc_lin
    assert acc_quad > 0.9, acc_quad
