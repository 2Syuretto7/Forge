# A bigram baseline, perplexity and bits per character

1. `bigram_probs(ids, V, alpha=1.0)`: the add-$\alpha$ smoothed table $P[a, b] = (c_{ab} + \alpha)/(c_a + \alpha V)$, where $c_{ab}$ counts $a$ followed by $b$ in `ids`.
2. `cross_entropy(ids, P)`: mean of $-\ln P[x_t, x_{t+1}]$ over the sequence.
3. `perplexity(nats_per_token)` and `bits_per_char(nats_per_token, n_tokens, n_chars)`.

Every language model should beat this baseline; the tests check the formulas on a small example.

## Hints

1. `np.add.at(C, (a, b), 1)` counts with repeated indices.
2. Each row of `P` sums to 1.
3. Total nats is `nats_per_token * n_tokens`; divide by characters, then by $\ln 2$.
