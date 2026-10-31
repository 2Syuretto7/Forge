import numpy as np
import sub

R = np.array([1.0, 2.0, 0.5, 3.0, 2.5])


def test_grad_value():
    for tau in (0.3, 1.0, 5.0):
        h = 1e-6
        num = np.array([(sub.value(R + h * e, tau) - sub.value(R - h * e, tau)) / (2 * h) for e in np.eye(5)])
        assert np.allclose(num, sub.gibbs(R, tau), atol=1e-8)


def test_optimality():
    rng = np.random.default_rng(8)
    for tau in (0.5, 2.0):
        p = sub.gibbs(R, tau)
        best = sub.objective(p, R, tau)
        assert abs(best - sub.value(R, tau)) < 1e-12
        for _ in range(100):
            assert sub.objective(rng.dirichlet(np.ones(5)), R, tau) <= best + 1e-12


def test_limits():
    assert sub.gibbs(R, 1e-3)[3] > 0.999
    assert np.allclose(sub.gibbs(R, 1e4), 0.2, atol=1e-3)
