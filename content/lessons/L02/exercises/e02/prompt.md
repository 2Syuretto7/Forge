# Train and test curves

For the target $f(x) = \sin(\pi x)$ with Gaussian noise, compute training and test error for a range of polynomial degrees.

- `curves(x_tr, y_tr, x_te, y_te, degrees)`: two arrays `(train_mse, test_mse)` of the same length as `degrees`.
- `best_degree(degrees, test_mse)`.

The tests check the classical shape: training error never increases with degree, and test error falls, then rises.

## Hints

1. Reuse the polynomial fit from exercise 1 (copy it in; each exercise is its own module).
2. Test error is measured against the noisy test targets.
3. `degrees[np.argmin(test_mse)]`.
