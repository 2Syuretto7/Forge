# Naive Bayes on 20,000 messages

The starter's `make_corpus(n_docs=20000, seed=0)` returns `(X, y)`: word counts for 300 words and labels, about a third spam. Spam messages often contain three fixed phrases, each a group of four words that occur together.

- `train_test(X, y, n_train)`: the first `n_train` rows for training, the rest for testing; return the four arrays.
- `accuracy(model, X, y)`: the fraction classified correctly at threshold $\frac12$.
- `evaluate(seed=0)`: build the corpus, train on 16,000 messages (the provided `fit` and `predict_proba`), and return the test accuracy.

## Hints

1. Slicing: `X[:n_train]`.
2. `np.mean((p > 0.5) == (y == 1))`.
3. The tests expect more than 95 percent.
