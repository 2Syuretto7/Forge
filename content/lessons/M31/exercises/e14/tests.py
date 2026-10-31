import numpy as np
import sub


def test_inflation_without_skill():
    rng = np.random.default_rng(1)
    labels = rng.integers(0, 2, 1000) * 2 - 1
    P = sub.random_predictions(1000, 1000, rng)
    vote = sub.adaptive_vote(P, labels)
    test_acc = sub.accuracy(vote, labels)
    keep = (P == labels).mean(axis=1) > 0.5
    fresh_labels = rng.integers(0, 2, 1000) * 2 - 1
    fresh = sub.random_predictions(1000, 1000, rng)
    fresh_vote = np.sign(fresh[keep].sum(axis=0) + 0.5)
    assert test_acc > 0.68, test_acc
    assert abs(sub.accuracy(fresh_vote, fresh_labels) - 0.5) < 0.05
