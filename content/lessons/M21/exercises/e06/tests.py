import numpy as np
import sub

rng = np.random.default_rng(6)
X = rng.poisson(1.0, size=(200, 12))
y = (X[:, 3] + X[:, 7] > 2).astype(int)
M = sub.fit(X, y)


def test_grad_linear_in_counts():
    c = rng.uniform(0, 3, size=12)
    s = sub.word_scores(M)
    for w in range(12):
        e = np.zeros(12)
        e[w] = 1e-6
        num = (sub.log_odds_counts(M, c + e) - sub.log_odds_counts(M, c - e)) / 2e-6
        assert abs(num - s[w]) < 1e-6


def test_top_words():
    assert set(sub.top_words(M, 2)) == {3, 7}
