import numpy as np
import sub

MEANS = np.array([0.0, 0.5, 1.0])


def test_offset_variance():
    rng = np.random.default_rng(0)
    z = np.zeros(3)
    v0 = sub.gradient_variance(z, MEANS, 20000, rng)
    v100 = sub.gradient_variance(z, MEANS + 100, 20000, rng)
    v100b = sub.gradient_variance(z, MEANS + 100, 20000, rng, b=100.5)
    assert v100 > 1000 * v0 and v100b < 2 * v0


def test_offset_training():
    no_base = np.mean([sub.train(MEANS, 100, 2000, 0.002, False, np.random.default_rng(s)) for s in range(3)])
    base = np.mean([sub.train(MEANS, 100, 2000, 0.05, True, np.random.default_rng(s)) for s in range(3)])
    assert base > 0.9 and no_base < 0.6, (base, no_base)
