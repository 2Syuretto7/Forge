import numpy as np
import sub

theta = np.array([0.2, -0.5, 1.0, 0.3])
r = np.array([1.0, 2.0, 0.5, 1.5]) + 10


def test_unbiased_and_lower_variance():
    p = sub.softmax(theta)
    m0, v0 = sub.estimator_stats(theta, r, 0.0)
    m1, v1 = sub.estimator_stats(theta, r, p @ r)
    m2, _ = sub.estimator_stats(theta, r, 3.0)
    assert np.allclose(m0, m1) and np.allclose(m0, m2)
    assert v1 < v0 / 50
