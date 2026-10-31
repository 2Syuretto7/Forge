import numpy as np
import sub

RAIN = np.array([[0.3, 0.05], [0.15, 0.5]])


def test_umbrella():
    assert np.allclose(sub.marginal(RAIN, 0), [0.35, 0.65]) and np.allclose(sub.marginal(RAIN, 1), [0.45, 0.55])
    c = sub.conditional_y_given_x(RAIN)
    assert np.allclose(c.sum(axis=1), 1) and abs(c[0, 0] - 0.3 / 0.35) < 1e-12
    assert not sub.is_independent(RAIN)


def test_round_trip_and_independence():
    rng = np.random.default_rng(1)
    J = rng.random((3, 4))
    J /= J.sum()
    assert np.allclose(sub.from_conditional(sub.marginal(J, 0), sub.conditional_y_given_x(J)), J)
    assert sub.is_independent(np.outer([0.2, 0.8], [0.1, 0.6, 0.3]))


def test_zero_row():
    try:
        sub.conditional_y_given_x(np.array([[0.5, 0.5], [0.0, 0.0]]))
    except ValueError:
        return
    raise AssertionError("expected ValueError")
