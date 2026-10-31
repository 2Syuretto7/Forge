import numpy as np
import sub

XS = np.array([-2.0, -0.7, 0.0, 0.4, 1.5])


def test_grad_heat_kernel():
    h = 1e-5
    for t in (0.3, 1.0, 2.5):
        num_x = (sub.heat_kernel(XS + h, t) - sub.heat_kernel(XS - h, t)) / (2 * h)
        num_xx = (sub.d_heat_dx(XS + h, t) - sub.d_heat_dx(XS - h, t)) / (2 * h)
        num_t = (sub.heat_kernel(XS, t + h) - sub.heat_kernel(XS, t - h)) / (2 * h)
        assert np.max(np.abs(num_x - sub.d_heat_dx(XS, t))) < 1e-7
        assert np.max(np.abs(num_xx - sub.d2_heat_dx2(XS, t))) < 1e-7
        assert np.max(np.abs(num_t - sub.d_heat_dt(XS, t))) < 1e-7


def test_heat_equation():
    for t in (0.3, 1.0, 2.5):
        assert np.allclose(sub.d_heat_dt(XS, t), 0.5 * sub.d2_heat_dx2(XS, t), atol=1e-14)


def test_brownian_limit():
    times, W = sub.scaled_walk(100, 2, 5000, np.random.default_rng(0))
    assert W.shape == (5000, 201) and times[100] == 1.0 and np.all(W[:, 0] == 0)
    for k in (50, 100, 200):
        assert abs(W[:, k].var() / times[k] - 1) < 0.06
    inc1, inc2 = W[:, 100] - W[:, 50], W[:, 200] - W[:, 100]
    assert abs(np.corrcoef(inc1, inc2)[0, 1]) < 0.05
    # Bins of width 0.4 hold exactly two of the values W(1) can take (multiples of 0.2).
    hist, edges = np.histogram(W[:, 100], bins=np.arange(-3.1, 3.11, 0.4), density=True)
    mids = (edges[:-1] + edges[1:]) / 2
    assert np.max(np.abs(hist - sub.heat_kernel(mids, 1.0))) < 0.03
