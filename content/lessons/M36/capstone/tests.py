import numpy as np
import sub


def exact_value(theta):
    P, R = sub.make_world()
    pi = sub.policy(theta)
    Ppi = np.einsum("sa,ast->st", pi, P)
    return np.linalg.solve(np.eye(25) - sub.GAMMA * Ppi, np.sum(pi * R, axis=1))[0]


def test_agent_and_variance():
    theta, V = sub.train()
    assert abs(exact_value(theta) - sub.optimal_value()) < 0.5
    r = sub.gradient_variance(theta, V)
    assert r["factor"] > 3 and abs(r["factor"] - r["without"] / r["with"]) < 1e-9
    a, b = r["means"]
    assert np.max(np.abs(a - b)) < 4 * np.sqrt(r["without"] / 400)


def test_report():
    text = sub.REPORT.lower()
    assert len(sub.REPORT.split()) >= 120
    for w in ("baseline", "variance", "unbiased", "episodes"):
        assert w in text, w
