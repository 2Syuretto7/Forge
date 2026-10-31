import numpy as np
import sub

W, M, S = np.array([0.4, 0.6]), np.array([-2.0, 1.5]), np.array([0.4, 0.6])


def test_grad_mixture_score():
    x = np.array([-30.0, -2.0, -0.3, 0.8, 4.0, 40.0])
    h = 1e-5
    num = (sub.mixture_logpdf(x + h, W, M, S) - sub.mixture_logpdf(x - h, W, M, S)) / (2 * h)
    assert np.all(np.isfinite(sub.mixture_logpdf(x, W, M, S)))
    assert np.max(np.abs(num - sub.mixture_score(x, W, M, S)) / (1 + np.abs(num))) < 1e-6


def test_responsibilities():
    R = sub.responsibilities(np.array([-2.0, 1.5]), W, M, S)
    assert np.allclose(R.sum(axis=1), 1) and R[0, 0] > 0.99 and R[1, 1] > 0.99
