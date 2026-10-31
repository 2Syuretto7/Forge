import numpy as np
import sub

X = np.random.default_rng(5).poisson(3.0, size=40)


def test_grad_score():
    h = 1e-6
    for lam in (0.5, 2.0, 3.3, 7.0):
        num = (sub.loglik(lam + h, X) - sub.loglik(lam - h, X)) / (2 * h)
        assert abs(num - sub.score(lam, X)) < 1e-5 * max(1, abs(num))
    assert abs(sub.score(sub.mle(X), X)) < 1e-9


def test_sampling_spread_matches_fisher():
    data = np.random.default_rng(6).poisson(3.0, size=(20000, 50))
    mles = data.mean(axis=1)
    assert abs(mles.std() * np.sqrt(sub.fisher_information(3.0, 50)) - 1) < 0.03
    ses = np.array([sub.standard_error(row) for row in data[:4000]])
    cover = np.mean(np.abs(mles[:4000] - 3.0) <= 1.96 * ses)
    assert 0.93 < cover < 0.965, cover


def test_degenerate():
    assert sub.mle([0, 0, 0]) == 0.0 and sub.standard_error([0, 0, 0]) == 0.0
