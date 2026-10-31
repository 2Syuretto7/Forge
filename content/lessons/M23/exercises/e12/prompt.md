# Choosing the shrinkage by validation

How much to shrink depends on how much data you have. Choose `alpha` the way you would choose any hyperparameter: on held-out data.

- `best_alpha(X_train, X_val, alphas)`: the `alpha` from the list that maximizes the held-out log-likelihood of e11. The starter provides `make_embeddings`, `fit`, `shrink`, `score(m, S, X_test, alpha)` (the average log-density of `X_test` under the shrunk fit) and `heldout_loglik`, which fits and scores in one call.
- `alpha_curve(sizes, alphas, seed=0)`: for each training size $n$, draw `make_embeddings(n, seed)` and a validation set `make_embeddings(1000, seed + 1000)`, and return the list of best alphas.

The tests show that the best alpha falls as the data grow: strong shrinkage at 300 vectors, little at 10,000.

## Hints

1. `max(alphas, key=lambda a: ...)`.
2. Fit once per training set and call `score` for every alpha: refitting 10,000 vectors for each alpha would take seconds in the browser.
3. With unlimited data the sample covariance is the truth, and any shrinkage only distorts it.
