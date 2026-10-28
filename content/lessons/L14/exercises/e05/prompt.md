# Training windows

1. `train_val_split(ids, frac=0.9)`: the first `frac` of the tokens for training, the rest for validation.
2. `get_batch(ids, ctx, batch, rng)`: draw `batch` start positions with `rng.integers(0, len(ids) - ctx, size=batch)` and return `x` (each row `ids[s:s + ctx]`) and `y` (the same windows shifted by one), as arrays of shape `(batch, ctx)`.
3. `tokens_per_epoch(n_tokens, ctx, batch)`: the number of steps needed to see `n_tokens` token positions once.

## Hints

1. Convert `ids` to an array once.
2. `y[b, t]` is the token that follows `x[b, t]`.
3. Splitting by position, not at random, keeps validation text unseen.
