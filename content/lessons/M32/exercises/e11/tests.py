import math
import numpy as np
import sub


def ess(x):
    x = x - x.mean()
    n = len(x)
    f = np.fft.rfft(x, 2 * n)
    ac = np.fft.irfft(f * np.conj(f))[:n]
    ac = ac / ac[0]
    s, k = 0.0, 1
    while k + 1 < n and ac[k] + ac[k + 1] >= 0:
        s += ac[k] + ac[k + 1]
        k += 2
    return n / (1 + 2 * s)


def rw(log_p, x, step, n, rng):
    out = np.empty((n, len(x)))
    lx, acc = log_p(x), 0
    for i in range(n):
        y = x + step * rng.standard_normal(len(x))
        ly = log_p(y)
        if math.log(rng.random()) < ly - lx:
            x, lx, acc = y, ly, acc + 1
        out[i] = x
    return out, acc / n


def test_grad_log_gauss():
    sc = np.array([0.5, 1.0, 2.0, 3.0])
    x = np.array([0.3, -1.2, 2.0, 0.7])
    h = 1e-6
    for i in range(4):
        e = np.zeros(4)
        e[i] = h
        num = (sub.log_gauss(x + e, sc) - sub.log_gauss(x - e, sc)) / (2 * h)
        assert abs(num - sub.grad_log_gauss(x, sc)[i]) < 1e-7


def test_samples_target():
    sc = np.linspace(0.5, 2.0, 5)
    lp, g = (lambda x: sub.log_gauss(x, sc)), (lambda x: sub.grad_log_gauss(x, sc))
    rng = np.random.default_rng(0)
    h, x = sub.tune_mala(lp, g, np.zeros(5), rng)
    s, acc = sub.mala_chain(lp, g, x, h, 30000, rng)
    assert 0.45 < acc < 0.7, acc
    assert np.max(np.abs(s.var(axis=0) / sc**2 - 1)) < 0.15


def test_beats_random_walk_in_50_dimensions():
    sc = np.linspace(0.5, 1.0, 50)
    lp, g = (lambda x: sub.log_gauss(x, sc)), (lambda x: sub.grad_log_gauss(x, sc))
    rng = np.random.default_rng(1)
    h, x = sub.tune_mala(lp, g, np.zeros(50), rng)
    sm, _ = sub.mala_chain(lp, g, x, h, 8000, rng)
    sr, _ = rw(lp, np.zeros(50), 2.38 / math.sqrt(50) * 0.5, 8000, rng)
    e_mala = min(ess(sm[:, j]) for j in range(50))
    e_rw = min(ess(sr[1000:, j]) for j in range(50))
    assert e_mala > 4 * e_rw, (e_mala, e_rw)
