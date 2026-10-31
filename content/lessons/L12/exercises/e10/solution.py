import numpy as np


def epoch_order(shard_sizes, epoch, seed):
    """The (shard, item) pairs of one epoch: shards in the order of
    np.random.default_rng([seed, epoch]).permutation, and inside shard s the items in the order of
    np.random.default_rng([seed, epoch, s]).permutation(shard_sizes[s])."""
    order = []
    for s in np.random.default_rng([seed, epoch]).permutation(len(shard_sizes)):
        s = int(s)
        order += [(s, int(i)) for i in np.random.default_rng([seed, epoch, s]).permutation(shard_sizes[s])]
    return order


def next_batch(shard_sizes, batch_size, seed, state):
    """state = {"epoch": e, "index": i}: the position of the next item. Return (batch, new_state):
    batch_size (shard, item) pairs, continuing into the next epoch when one runs out."""
    epoch, index = state["epoch"], state["index"]
    batch = []
    order = epoch_order(shard_sizes, epoch, seed)
    while len(batch) < batch_size:
        if index == len(order):
            epoch, index = epoch + 1, 0
            order = epoch_order(shard_sizes, epoch, seed)
        take = min(batch_size - len(batch), len(order) - index)
        batch += order[index:index + take]
        index += take
    return batch, {"epoch": epoch, "index": index}
