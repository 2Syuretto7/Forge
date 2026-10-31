# Break it: resuming a shuffle buffer

Streaming loaders often shuffle with a buffer: read items into a buffer of fixed size and emit a random one each step. `naive_resume` shows a common bug: after a restart it skips the items already read and starts a new buffer with the original seed. Items that were sitting in the buffer are lost, and the random choices replay from the start.

1. `shuffle_step(stream, state)` with `state = {"pos", "buffer", "rng", "size"}`: top the buffer up from `stream[pos:]` to `size` items, then remove and return the item at `rng.integers(len(buffer))`; return `None` when both are exhausted.
2. `new_state(buffer_size, seed)`: position 0, an empty buffer and `np.random.default_rng(seed)`.
3. `checkpoint(state)`: a copy of everything needed to resume: position, buffer and `rng.bit_generator.state`.
4. `restore(saved)`: a live state from a checkpoint.

## Hints

1. Copy the buffer list in both `checkpoint` and `restore`, so later steps cannot change the saved one.
2. `rng.bit_generator.state` is a dictionary; assigning it to a new generator's `bit_generator.state` continues the same random sequence.
3. The test compares a resumed run with an uninterrupted one, item by item.
