# A resumable sharded loader

Training data lives in shards. A loader must visit every example once per epoch in a shuffled order, and after a crash it must continue **exactly** where it stopped, or the resumed run sees some examples twice and others never.

1. `epoch_order(shard_sizes, epoch, seed)`: the list of (shard, item) pairs for one epoch: shards in the order of `np.random.default_rng([seed, epoch]).permutation(len(shard_sizes))`, and the items of shard $s$ in the order of `np.random.default_rng([seed, epoch, s]).permutation(shard_sizes[s])`.
2. `next_batch(shard_sizes, batch_size, seed, state)` with `state = {"epoch": e, "index": i}`: the next `batch_size` pairs and the new state, continuing into the next epoch when one runs out.

The order depends only on `(seed, epoch)`, so the state needs just two integers.

## Hints

1. Convert numpy integers with `int(...)` so states and pairs compare and serialize cleanly.
2. When `index` reaches the end of the epoch's order, move to epoch $e + 1$, index 0.
3. Never draw from a generator whose state you do not save: derive every permutation from `(seed, epoch, ...)`.
