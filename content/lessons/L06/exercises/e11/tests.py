import numpy as np
import sub


def test_winner_looks_good():
    best, _ = sub.best_of_m(500, 100, seed=3)
    assert best >= 0.62, best
    assert abs(best - sub.expected_max_accuracy(500, 100)) < 0.06


def test_winner_is_a_coin_flip_on_fresh_data():
    accs = [sub.fresh_accuracy(2000, seed=s) for s in range(5)]
    assert abs(np.mean(accs) - 0.5) < 0.03


def test_more_models_more_optimism():
    a = np.mean([sub.best_of_m(10, 100, s)[0] for s in range(20)])
    b = np.mean([sub.best_of_m(1000, 100, s)[0] for s in range(20)])
    assert b > a + 0.04
