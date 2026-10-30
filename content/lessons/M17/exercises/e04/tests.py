import math
import numpy as np
import sub


def test_values():
    x, F = sub.cumulative(np.cos, 0, math.pi / 2, 2000)
    assert abs(F[-1] - 1) < 1e-6 and F[0] == 0
    assert np.allclose(F, np.sin(x), atol=1e-6)


def test_grad_fundamental_theorem():
    for f in (np.exp, np.cos, lambda t: 1 / (1 + t * t)):
        x, F = sub.cumulative(f, -1, 2, 4000)
        d = sub.derivative_of_cumulative(x, F)
        assert np.max(np.abs(d - f(x[1:-1]))) < 5e-6
