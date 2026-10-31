import numpy as np
import sub

X = np.array([-30.0, -3.0, -0.5, 0.0, 0.7, 4.0, 25.0])


def test_grad_softplus_and_log_sigmoid():
    h = 1e-6
    num = (sub.softplus(X + h) - sub.softplus(X - h)) / (2 * h)
    assert np.allclose(num, sub.sigmoid(X), atol=1e-9)
    num = (sub.log_sigmoid(X + h) - sub.log_sigmoid(X - h)) / (2 * h)
    assert np.allclose(num, sub.sigmoid(-X), atol=1e-9)


def test_extremes_without_overflow():
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        assert sub.softplus(1000.0) == 1000.0 and sub.softplus(-1000.0) == 0.0
        assert abs(sub.softplus(-40.0) - 4.248354255291589e-18) < 1e-30
        assert sub.sigmoid(1000.0) == 1.0 and sub.sigmoid(-1000.0) == 0.0
        assert abs(sub.log_sigmoid(40.0) + 4.248354255291589e-18) < 1e-30
        assert sub.log_sigmoid(-1000.0) == -1000.0


def test_shapes():
    assert sub.sigmoid(np.zeros((2, 3))).shape == (2, 3)
    assert abs(float(sub.sigmoid(0.0)) - 0.5) < 1e-15
