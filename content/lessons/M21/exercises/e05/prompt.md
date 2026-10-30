# Training naive Bayes

Documents are rows of a count matrix `X` (shape `(n_docs, V)`: `X[i, w]` is how often word `w` occurs in document `i`) with labels `y` in {0, 1}.

- `fit(X, y, alpha=1.0)`: return a dictionary with `"log_prior"` (shape `(2,)`) and `"log_word"` (shape `(2, V)`), where $\log P(w \mid c) = \log\frac{\text{count}_c(w) + \alpha}{\sum_{w'} (\text{count}_c(w') + \alpha)}$.
- `log_odds(model, X)`: for each row, $\log P(1 \mid \text{doc}) - \log P(0 \mid \text{doc})$: the prior log-ratio plus the counts times the word log-ratios.
- `predict_proba(model, X)`: the probability of class 1, the sigmoid of the log-odds.

## Hints

1. `X[y == c].sum(axis=0) + alpha` for each class.
2. `X @ (log_word[1] - log_word[0])`.
3. `1 / (1 + np.exp(-z))`; for very negative `z` use `np.exp(z) / (1 + np.exp(z))` or clip.
