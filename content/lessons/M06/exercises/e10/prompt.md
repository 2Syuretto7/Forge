# Softmax over a vocabulary

Use NumPy arrays now: a vocabulary of $V = 50{,}000$ tokens means 50,000 scores.

- `log_softmax(logits)`: for a 1-D array, `logits - logsumexp`, with the max shift, fully vectorized.
- `cross_entropy(logits, target)`: minus the log-softmax at index `target`.
- `uniform_loss(V)`: the loss of a model whose scores are all equal, $\ln V$.
- `random_init_loss(V, scale, seed=0)`: the average cross-entropy over 100 random targets for logits drawn as `scale` times standard normal noise (one logits vector per target), with `np.random.default_rng(seed)`.

A freshly initialized language model has small random logits, so its first loss is close to $\ln V$. If your first training step reports a loss far above that, something is wrong before training even starts.

## Hints

1. `m = logits.max(); return logits - (m + np.log(np.exp(logits - m).sum()))`.
2. `-log_softmax(logits)[target]`.
3. Draw `rng.normal(size=V) * scale` and `rng.integers(V)` inside a loop of 100.
