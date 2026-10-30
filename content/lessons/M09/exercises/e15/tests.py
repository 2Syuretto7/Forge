import numpy as np
import sub


def u(deg):
    t = np.radians(deg)
    return np.array([np.cos(t), np.sin(t)])


def test_cosine_distance_violates():
    assert abs(sub.triangle_violation(sub.cosine_distance, u(0), u(60), u(120)) - 0.5) < 1e-12
    trip = sub.find_violation(sub.cosine_distance)
    assert trip is not None
    assert sub.triangle_violation(sub.cosine_distance, *trip) > 0


def test_angle_is_a_metric():
    assert sub.find_violation(sub.angular_distance, trials=3000) is None
