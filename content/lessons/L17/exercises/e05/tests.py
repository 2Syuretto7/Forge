import numpy as np
import sub

logp_old = np.log(np.array([0.2, 0.5, 0.1, 0.3, 0.25]))
logp = np.log(np.array([0.3, 0.45, 0.05, 0.31, 0.21]))
adv = np.array([1.0, -1.0, 2.0, 0.5, -0.5])


def test_grad_ppo():
    _, g = sub.ppo_objective(logp, logp_old, adv, 0.2)
    num = []
    for i in range(5):
        e = np.zeros(5)
        e[i] = 1e-7
        num.append((sub.ppo_objective(logp + e, logp_old, adv, 0.2)[0] - sub.ppo_objective(logp - e, logp_old, adv, 0.2)[0]) / 2e-7)
    assert np.allclose(g, num, atol=1e-6)


def test_clipping():
    obj, g = sub.ppo_objective(np.log([0.3]), np.log([0.2]), np.array([1.0]), 0.2)
    assert abs(obj - 1.2) < 1e-12 and g[0] == 0
    obj, g = sub.ppo_objective(np.log([0.3]), np.log([0.2]), np.array([-1.0]), 0.2)
    assert abs(obj + 1.5) < 1e-12 and abs(g[0] + 1.5) < 1e-12
