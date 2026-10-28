import numpy as np
import sub

theta = np.array([0.2, -0.5, 1.0])
r = np.array([1.0, 2.0, 0.5])


def test_grad_expected_reward():
    g = sub.exact_policy_gradient(theta, r)
    J = lambda t: sub.softmax(t) @ r
    num = [(J(theta + e) - J(theta - e)) / 2e-6 for e in np.eye(3) * 1e-6]
    assert np.allclose(g, num, atol=1e-9)


def test_score_sums_to_zero_in_expectation():
    p = sub.softmax(theta)
    assert np.allclose(sum(p[a] * sub.score(theta, a) for a in range(3)), 0)


def test_sampled_estimate():
    est = sub.reinforce_estimate(theta, r, 20000, 0, baseline=1.0)
    assert np.allclose(est, sub.exact_policy_gradient(theta, r), atol=0.01)
