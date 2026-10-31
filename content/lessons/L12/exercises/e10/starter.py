import numpy as np


def epoch_order(shard_sizes, epoch, seed):
    """The (shard, item) pairs of one epoch: shards in the order of
    np.random.default_rng([seed, epoch]).permutation, and inside shard s the items in the order of
    np.random.default_rng([seed, epoch, s]).permutation(shard_sizes[s])."""
    raise NotImplementedError


def next_batch(shard_sizes, batch_size, seed, state):
    """state = {"epoch": e, "index": i}: the position of the next item. Return (batch, new_state):
    batch_size (shard, item) pairs, continuing into the next epoch when one runs out."""
    raise NotImplementedError
