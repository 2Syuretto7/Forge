import numpy as np
import sub

p = np.array([0.5, 0.3, 0.15, 0.05])
q = np.array([0.2, 0.5, 0.2, 0.1])


def test_distribution_preserved():
    assert np.allclose(sub.emitted_distribution(p, q), p)
    assert np.allclose(sub.emitted_distribution(p, p), p)
    assert abs(sub.acceptance_rate(p, q) - 0.7) < 1e-12


def test_grad_acceptance():
    z = np.log(q) + 0.1
    g = sub.acceptance_grad(p, z)
    num = []
    for i in range(4):
        e = np.zeros(4)
        e[i] = 1e-6
        f = lambda zz: sub.acceptance_rate(p, np.exp(zz) / np.exp(zz).sum())
        num.append((f(z + e) - f(z - e)) / 2e-6)
    assert np.allclose(g, num, atol=1e-8)


def test_expected_tokens():
    assert sub.expected_tokens(0.0, 4) == 1.0 and sub.expected_tokens(1.0, 4) == 5
    assert abs(sub.expected_tokens(0.8, 4) - (1 - 0.8 ** 5) / 0.2) < 1e-12
