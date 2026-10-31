import math
import numpy as np


def duplicated_accuracies(p, unique, copies, sets, rng):
    """Measured accuracies of test sets made of copied examples."""
    raise NotImplementedError


def naive_coverage(accs, p, rows, delta=0.05):
    """Coverage of Hoeffding intervals that assume rows independent examples."""
    raise NotImplementedError


def effective_n(rows, copies):
    """Independent examples behind a duplicated test set."""
    raise NotImplementedError
