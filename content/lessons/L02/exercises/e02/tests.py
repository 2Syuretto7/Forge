import math
import numpy as np
import sub

rng = np.random.default_rng(2)
U = rng.uniform(size=200000)
U2 = rng.uniform(size=200000)


def test_categorical_is_deterministic_and_correct():
    p = np.array([0.2, 0.5, 0.3])
    assert list(sub.sample_categorical(p, np.array([0.0, 0.19, 0.2, 0.69, 0.71, 0.999]))) == [0, 0, 1, 1, 2, 2]
    counts = np.bincount(sub.sample_categorical(p, U), minlength=3) / U.size
    assert np.allclose(counts, p, atol=0.005), counts


def test_exponential_moments():
    x = sub.sample_exponential(2.0, U)
    assert x.min() >= 0
    assert abs(x.mean() - 0.5) < 0.005
    assert abs(x.var() - 0.25) < 0.01


def test_box_muller_is_standard_normal():
    z1, z2 = sub.box_muller(1 - U, U2)
    z = np.concatenate([z1, z2])
    assert abs(z.mean()) < 0.01 and abs(z.std() - 1) < 0.01
    for q in [-1.96, -1.0, 0.0, 1.0, 1.96]:
        emp = np.mean(z <= q)
        assert abs(emp - 0.5 * (1 + math.erf(q / math.sqrt(2)))) < 0.005


def test_box_muller_pairs_are_uncorrelated():
    z1, z2 = sub.box_muller(1 - U, U2)
    assert abs(np.corrcoef(z1, z2)[0, 1]) < 0.01
