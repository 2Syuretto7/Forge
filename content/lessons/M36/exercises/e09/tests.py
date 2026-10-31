import numpy as np
import sub

MEANS = np.array([5.0, 5.2, 5.4, 5.6, 6.0])


def test_learns_the_best_arm():
    probs = [sub.train_bandit(MEANS, 3000, 0.05, True, np.random.default_rng(s)) for s in range(3)]
    assert all(abs(p.sum() - 1) < 1e-12 for p in probs)
    assert np.mean([sub.best_arm_prob(p, MEANS) for p in probs]) > 0.8
