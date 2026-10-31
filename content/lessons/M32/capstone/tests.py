import math
import numpy as np
import sub


def reference():
    x, y = sub.make_data()
    A, B = np.meshgrid(np.linspace(-1.6, 2.3, 241), np.linspace(-0.8, 4.6, 241), indexing="ij")
    z = A.ravel()[:, None] + B.ravel()[:, None] * x[None, :]
    lp = np.sum(y * z - np.logaddexp(0, z), axis=1) - 0.5 * (A.ravel() ** 2 + B.ravel() ** 2) / 25
    w = np.exp(lp - lp.max())
    w /= w.sum()
    th = np.stack([A.ravel(), B.ravel()], axis=1)
    mean = w @ th
    sd = np.sqrt(w @ (th - mean) ** 2)
    return mean, sd


def test_log_post_and_gradient():
    th = np.array([0.2, 1.1])
    stack = np.array([[0.2, 1.1], [0.0, 0.0], [1.0, 2.0]])
    vals = sub.log_post(stack)
    assert isinstance(sub.log_post(th), float) and abs(vals[0] - sub.log_post(th)) < 1e-12
    assert vals.shape == (3,)
    h = 1e-6
    g = sub.grad_log_post(th)
    for i in range(2):
        e = np.zeros(2)
        e[i] = h
        assert abs((sub.log_post(th + e) - sub.log_post(th - e)) / (2 * h) - g[i]) < 1e-5


def test_matches_reference():
    samples, acc = sub.run_chains()
    assert samples.shape == (4, 5000, 2) and 0.1 < acc < 0.8
    d = sub.diagnostics(samples)
    mean, sd = reference()
    for j in range(2):
        assert abs(d["mean"][j] - mean[j]) < 4 * d["mcse"][j] + 1e-3, (j, d["mean"][j], mean[j])
        assert abs(d["sd"][j] / sd[j] - 1) < 0.06
        assert d["r_hat"][j] < 1.01 and d["ess"][j] > 1000
    assert d["acf"].shape == (2, 51) and np.allclose(d["acf"][:, 0], 1) and np.all(d["acf"][:, 50] < 0.1)


def test_report():
    text = sub.REPORT.lower()
    assert len(sub.REPORT.split()) >= 120
    for word in ("acceptance", "effective sample size", "r-hat", "trace", "autocorrelation"):
        assert word in text, word
