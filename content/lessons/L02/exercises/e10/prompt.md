# Break it: feature selection outside the cross-validation loop

Build the leak of Movement 5 from pure noise: `X` is `(50, 1000)` noise, labels are random 0/1.

- `top_k_features(X, y, k)`: indices of the `k` columns with the largest absolute correlation with `y`.
- `centroid_classifier(Xtr, ytr, Xte)`: predict the class whose training mean is nearer (Euclidean) to each test row.
- `cv_accuracy(X, y, k, folds, seed, leaky)`: 5-fold style CV with `np.random.default_rng(seed).permutation` folds. If `leaky`, select features once on all the data before splitting; otherwise select inside each training fold. Return the mean validation accuracy.

## Hints

1. Correlation: center columns and `y`, then `(Xc * yc[:, None]).sum(0) / (norms)`.
2. `np.argsort(-np.abs(corr))[:k]`.
3. The only difference between the two modes is which rows the selection sees.
