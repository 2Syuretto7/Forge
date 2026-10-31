import numpy as np
import sub

rng = np.random.default_rng(9)
n = 5
lw, ll = rng.normal(size=n) - 2, rng.normal(size=n) - 2
lw_ref, ll_ref = rng.normal(size=n) - 2, rng.normal(size=n) - 2


def test_grad_dpo():
    _, gw, gl = sub.dpo_loss(lw, ll, lw_ref, ll_ref, 0.5)
    for vec, g, which in [(lw, gw, 0), (ll, gl, 1)]:
        num = []
        for i in range(n):
            e = np.zeros(n)
            e[i] = 1e-6
            args = [lw, ll]
            args[which] = vec + e
            up = sub.dpo_loss(args[0], args[1], lw_ref, ll_ref, 0.5)[0]
            args[which] = vec - e
            num.append((up - sub.dpo_loss(args[0], args[1], lw_ref, ll_ref, 0.5)[0]) / 2e-6)
        assert np.allclose(g, num, atol=1e-8)


def test_dpo_finds_the_kl_optimum():
    ref = np.array([0.4, 0.3, 0.2, 0.1])
    r = np.array([0.0, 1.0, 2.0, 0.5])
    prefs = [(i, j, 1 / (1 + np.exp(-(r[i] - r[j])))) for i in range(4) for j in range(4) if i != j]
    pi = sub.tabular_dpo(ref, prefs, 0.5)
    opt = ref * np.exp(r / 0.5)
    assert np.allclose(pi, opt / opt.sum(), atol=1e-4)
