# Standardization without leakage

Section 5 says: compute feature means and standard deviations on the **training** split and apply them to both splits.

- `fit_standardizer(X_train)`: returns `(mean, std)`; replace any zero standard deviation by 1 so constant features do not cause division by zero.
- `transform(X, mean, std)`.
- `fit_transform_both(X_train, X_test)`: returns the transformed train and test arrays, using training statistics only.

## Hints

1. `X_train.mean(axis=0)`, `X_train.std(axis=0)`.
2. `np.where(std == 0, 1.0, std)`.
3. After transformation the training columns have mean 0 and standard deviation 1; the test columns will be close but not exact, and that is correct.
