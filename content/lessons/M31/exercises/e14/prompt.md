# Break it: adaptive overfitting

Selecting the best model is mild. Combining models adaptively, using the test set as a guide, can push test accuracy far above anything the models can do. Take $k = 1000$ random-guessing classifiers that predict labels $\pm1$ at random, keep those that score above $\frac12$ on the test set, and take their majority vote (Section 2).

- `random_predictions(k, n, rng)`: a `(k, n)` array of random $\pm1$ predictions.
- `adaptive_vote(P, labels)`: the majority vote, over the rows of `P` whose test accuracy exceeds $\frac12$, as an array of $\pm1$ (ties to $+1$).
- `accuracy(pred, labels)`.

The tests reach about 73 percent test accuracy with no skill at all, while the same recipe on fresh examples (fresh labels and fresh random predictions from the same classifiers, which still guess) scores about 50 percent.

## Hints

1. `np.sign(P[keep].sum(axis=0) + 0.5)` breaks ties to $+1$.
2. Each kept classifier is slightly correlated with the test labels by selection; the vote adds up those small correlations.
3. This is why benchmarks hide their test labels and limit submissions.
