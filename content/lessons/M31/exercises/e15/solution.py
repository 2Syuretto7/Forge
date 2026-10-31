import math
import numpy as np


def duplicated_accuracies(p, unique, copies, sets, rng):
    """Measured accuracies of test sets made of copied examples."""
    distinct = rng.random((sets, unique)) < p
    return np.repeat(distinct, copies, axis=1).mean(axis=1)


def naive_coverage(accs, p, rows, delta=0.05):
    """Coverage of Hoeffding intervals that assume rows independent examples."""
    h = math.sqrt(math.log(2 / delta) / (2 * rows))
    return float(np.mean(np.abs(np.asarray(accs) - p) <= h))


def effective_n(rows, copies):
    """Independent examples behind a duplicated test set."""
    return rows // copies
