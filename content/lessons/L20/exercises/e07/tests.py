import numpy as np
import sub

rng = np.random.default_rng(3)
lc, lr, rc, rr = (rng.normal(size=5) * 3 for _ in range(4))


def test_grad_dpo():
    _, gc, gr = sub.dpo_loss(lc, lr, rc, rr, 0.1)
    e = np.eye(5) * 1e-6
    numc = [(sub.dpo_loss(lc + d, lr, rc, rr, 0.1)[0] - sub.dpo_loss(lc - d, lr, rc, rr, 0.1)[0]) / 2e-6 for d in e]
    numr = [(sub.dpo_loss(lc, lr + d, rc, rr, 0.1)[0] - sub.dpo_loss(lc, lr - d, rc, rr, 0.1)[0]) / 2e-6 for d in e]
    assert np.allclose(gc, numc, atol=1e-9) and np.allclose(gr, numr, atol=1e-9)


def test_values():
    assert abs(sub.dpo_loss(rc, rr, rc, rr, 0.5)[0] - np.log(2)) < 1e-12
    assert abs(sub.implied_reward(-3.0, -5.0, 0.1) - 0.2) < 1e-12
    big = sub.dpo_loss(np.array([1000.0]), np.array([0.0]), np.array([0.0]), np.array([0.0]), 1.0)
    assert np.isfinite(big[0]) and big[0] < 1e-12
