import numpy as np


def best_of_m(M, n_test, seed=0):
    rng = np.random.default_rng(seed)
    y = rng.integers(0, 2, size=n_test)
    P = rng.integers(0, 2, size=(M, n_test))
    accs = (P == y).mean(axis=1)
    i = int(np.argmax(accs))
    return float(accs[i]), i


def fresh_accuracy(n_fresh, seed=1):
    rng = np.random.default_rng(seed)
    y = rng.integers(0, 2, size=n_fresh)
    p = rng.integers(0, 2, size=n_fresh)
    return float(np.mean(p == y))


def expected_max_accuracy(M, n_test):
    return 0.5 + np.sqrt(2 * np.log(M)) * 0.5 / np.sqrt(n_test)
