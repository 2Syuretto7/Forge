# Bits per character under n-gram models

How many bits per character does a text need? It depends on the model: one that knows nothing but letter frequencies, or one that also knows the previous letter, or the previous two. The starter's `make_corpus(n_chars, seed=0)` returns English-like text built from real words, lowercase, with spaces and full stops.

- `ngram_model(text, n)`: two `Counter`s, one for every $n$-character string in `text` and one for every $(n-1)$-character context that precedes a character (for $n = 1$ the context is the empty string).
- `cross_entropy_bits(train, test, n, k=0.1)`: the average of $-\log_2 q(c \mid \text{context})$ over the characters of `test` from position $n - 1$ on, where $q$ is the **add-$k$** smoothed estimate $\frac{\text{count}(\text{context}, c) + k}{\text{count}(\text{context}) + kV}$ from `train`, and $V$ is the number of distinct characters in `train` and `test` together.
- `bits_table(train, test, orders=(1, 2, 3, 4))`: a dict from order to cross-entropy.

The tests train on 180,000 characters and test on the next 20,000: each extra character of context lowers the cost, from about 4 bits to about 1.5. Then they train on only 2,000 characters, where the 4-gram model has seen too few of its contexts and does worse than the trigram.

## Hints

1. `text[i - n + 1:i + 1]` is the $n$-gram ending at position `i`, and `text[i - n + 1:i]` its context.
2. A `Counter` returns 0 for a missing key, which is exactly what smoothing needs.
3. Cross-entropy on held-out text is the honest measure: on the training text itself, higher orders always look better.
