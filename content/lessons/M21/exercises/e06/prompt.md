# Log-odds are linear in the counts

Naive Bayes scores a document by adding one log-ratio per word occurrence.

- `word_scores(model)`: the vector $\log P(w \mid 1) - \log P(w \mid 0)$ (the provided `fit` builds the model).
- `log_odds_counts(model, counts)`: the log-odds for a count vector, allowing fractional counts.
- `top_words(model, k)`: the indices of the `k` words with the largest scores, largest first.

The tests run a **gradient check**: the derivative of the log-odds with respect to each count, by central differences on fractional counts, is that word's score.

## Hints

1. Subtract the two rows of `log_word`.
2. `log_prior[1] - log_prior[0] + counts @ scores`.
3. `np.argsort(-scores)[:k]`.
