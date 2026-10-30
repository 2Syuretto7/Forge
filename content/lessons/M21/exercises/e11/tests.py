import numpy as np
import sub


def test_calibrated_predictor():
    rng = np.random.default_rng(11)
    p = rng.random(100_000)
    y = (rng.random(100_000) < p).astype(int)
    assert sub.ece(p, y) < 0.01
    assert sum(c for *_, c in sub.reliability(p, y)) == 100_000


def test_naive_bayes_is_overconfident():
    p, y = sub.nb_probabilities()
    assert sub.ece(p, y) > 0.01
    assert sub.overconfidence(p, y) > 0.01
