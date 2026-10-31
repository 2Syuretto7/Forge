# Break it: temperature extremes

A bigram table `P` (rows are next-token distributions) stands in for a trained model.

1. `generate(P, start, n, T, rng)`: sample `n` tokens after `start` at temperature `T`, using $p_T \propto P^{1/T}$ (dividing the log-probabilities by `T`).
2. `distinct_ratio(seq, n=3)`: distinct `n`-grams divided by all `n`-grams in `seq`.
3. `model_nll(seq, P)`: the mean negative log-likelihood of `seq` under the untempered `P`.

Low temperature loops (few distinct trigrams); high temperature produces sequences the model itself finds unlikely (high negative log-likelihood).

## Hints

1. Subtract the maximum of the tempered log-probabilities before exponentiating.
2. Use `tuple(seq[i:i + n])` as the n-gram key.
3. Compare temperatures 0.1, 1 and 5 on the same table and seed.
