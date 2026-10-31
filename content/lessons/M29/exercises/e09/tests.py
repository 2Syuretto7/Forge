import numpy as np
import sub


def test_constant_gradient():
    mh, vh = sub.adam_moments([3.0] * 50)
    assert np.allclose(mh, 3.0) and np.allclose(vh, 9.0)
    for scale in (1e-3, 1.0, 1e3):
        xs = sub.adam(lambda x: np.full(2, scale), np.zeros(2), 0.01, 5)
        steps = np.abs(np.diff(np.array(xs), axis=0))
        assert np.allclose(steps, 0.01, rtol=1e-4), (scale, steps)


def test_badly_scaled_quadratic():
    s = np.array([1e-2, 1e2])
    grad = lambda x: s * s * x
    xs = sub.adam(grad, np.array([1.0, 1.0]), 0.01, 3000)
    assert np.all(np.abs(xs[-1]) < 0.05), xs[-1]
