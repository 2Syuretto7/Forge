import numpy as np
import sub


def test_probs():
    ids = [0, 1, 0, 1, 1, 2]
    P = sub.bigram_probs(ids, 3, alpha=1.0)
    assert np.allclose(P.sum(axis=1), 1)
    assert np.isclose(P[0, 1], (2 + 1) / (2 + 3)) and np.isclose(P[2, 0], 1 / 3)
    P0 = sub.bigram_probs(ids, 3, alpha=0.0 + 1e-12)
    assert np.isclose(P0[1, 0], 1 / 3, atol=1e-9)


def test_loss_units():
    ids = [0, 1, 0, 1]
    P = np.full((2, 2), 0.5)
    assert np.isclose(sub.cross_entropy(ids, P), np.log(2))
    assert np.isclose(sub.perplexity(np.log(2)), 2.0)
    assert np.isclose(sub.bits_per_char(1.5, 1000, 2000), 1.5 / 2 / np.log(2))


def test_validation_is_worse_than_training():
    rng = np.random.default_rng(6)
    ids = rng.integers(0, 20, size=400)
    P = sub.bigram_probs(ids[:300], 20)
    assert sub.cross_entropy(ids[300:], P) > sub.cross_entropy(ids[:300], P)
