import numpy as np
import sub


def test_finds_the_best_arm():
    p = sub.train_bandit([0.0, 0.5, 1.0, 0.2], 300, 0.5, 0)
    assert p.argmax() == 2 and p[2] > 0.9 and abs(p.sum() - 1) < 1e-12
