# Choosing the degree by cross-validation

- `select_degree(x, y, degrees, k, seed)`: return the degree with the lowest `cv_mse` (reuse exercise 5), breaking ties toward the smaller degree.
- `refit(x, y, degree)`: refit on all the training data.

The test then evaluates the selected model on a large fresh test set and requires it to be within 20 percent of the best possible degree's test error.

## Hints

1. Loop over the degrees and keep the best score.
2. Use strict comparison `<` so ties keep the earlier, smaller degree.
3. Refit on everything once the degree is chosen: the folds were only for choosing.
