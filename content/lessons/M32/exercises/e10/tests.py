import numpy as np
import sub

X, Y = sub.make_data()


def test_grad_log_posterior():
    rng = np.random.default_rng(0)
    w = rng.standard_normal(50)
    g = sub.grad_log_posterior(w, X, Y, 0.8, 1.5)
    h = 1e-6
    for i in rng.choice(50, 8, replace=False):
        e = np.zeros(50)
        e[i] = h
        num = (sub.log_posterior(w + e, X, Y, 0.8, 1.5) - sub.log_posterior(w - e, X, Y, 0.8, 1.5)) / (2 * h)
        assert abs(num - g[i]) < 1e-4 * max(1, abs(g[i]))


def test_exact():
    mu, cov = sub.exact_posterior(X, Y)
    assert np.max(np.abs(sub.grad_log_posterior(mu, X, Y))) < 1e-7
    assert np.allclose(cov, cov.T) and np.min(np.linalg.eigvalsh(cov)) > 0


def test_tuned_sampler():
    mu, cov = sub.exact_posterior(X, Y)
    sd = np.sqrt(np.diag(cov))
    rng = np.random.default_rng(1)
    lp = lambda w: sub.log_posterior(w, X, Y)
    step, x = sub.tune_rw(lp, np.zeros(50), rng)
    s, acc = sub.rw_chain(lp, x, step, 20000, rng)
    assert 0.17 < acc < 0.32, acc
    err = (s.mean(axis=0) - mu) / sd
    assert np.sqrt(np.mean(err**2)) < 0.35
