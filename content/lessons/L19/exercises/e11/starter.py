import numpy as np


def batch_ids(seed, epoch, n_examples, batch_size):
    """The batches of one epoch: a permutation fixed by (seed, epoch), cut into batches."""
    order = np.random.default_rng([seed, epoch]).permutation(n_examples)
    return [tuple(int(i) for i in order[j:j + batch_size]) for j in range(0, n_examples, batch_size)]


def buggy_resume(seed, epoch, batch_index, n_examples, batch_size, count):
    """A resume that restarts the epoch from the beginning instead of at batch_index."""
    out = []
    while len(out) < count:
        out += batch_ids(seed, epoch, n_examples, batch_size)
        epoch += 1
    return out[:count]


def stream(seed, epoch, batch_index, n_examples, batch_size, count):
    """The next `count` batches starting at batch_index of epoch, continuing into later epochs."""
    raise NotImplementedError


def first_divergence(reference, resumed):
    """The first index where two batch sequences differ, or None if they agree."""
    raise NotImplementedError
