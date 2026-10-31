import numpy as np
import sub


def test_known_entropies():
    assert abs(sub.entropy([0.5, 0.5], 2) - 1) < 1e-12
    assert abs(sub.entropy([0.5, 0.25, 0.25], 2) - 1.5) < 1e-12
    assert abs(sub.entropy(np.full(70, 1 / 70), np.e) - np.log(70)) < 1e-12


def test_zero_probabilities():
    assert sub.entropy([1.0, 0.0, 0.0]) == 0.0
    s = sub.surprisal(np.array([1.0, 0.0]))
    assert s[0] == 0 and np.isinf(s[1])


def test_bounds():
    rng = np.random.default_rng(1)
    for _ in range(50):
        p = rng.dirichlet(np.ones(6))
        h = sub.entropy(p, 2)
        assert -1e-12 <= h <= np.log2(6) + 1e-12


def test_units():
    assert abs(sub.to_bits(1.5) - 2.1640425613) < 1e-9
    p = np.array([0.1, 0.2, 0.7])
    assert abs(sub.to_bits(sub.entropy(p, np.e)) - sub.entropy(p, 2)) < 1e-12
