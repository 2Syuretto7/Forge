import numpy as np
import sub

X = np.array([[2, 0, 1], [3, 1, 0], [0, 2, 2], [1, 3, 1]])
y = np.array([0, 0, 1, 1])


def test_fit():
    m = sub.fit(X, y)
    assert np.allclose(np.exp(m["log_prior"]), [0.5, 0.5])
    assert np.allclose(np.exp(m["log_word"][0]), np.array([6, 2, 2]) / 10)
    assert np.allclose(np.exp(m["log_word"]).sum(axis=1), 1)


def test_predict():
    m = sub.fit(X, y)
    p = sub.predict_proba(m, X)
    assert np.all((p > 0.5) == (y == 1))
    z = sub.log_odds(m, np.array([[0, 1, 0]]))
    assert np.isclose(z[0], np.log((6 / 12) / (2 / 10)))
