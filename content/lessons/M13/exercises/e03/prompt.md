# Shift and invert

- `inverse_iteration(A, mu, iters=50, seed=0)`: power iteration on $(A - \mu I)^{-1}$, computed by solving $(A - \mu I)y = x$ at each step (never form the inverse), starting from a seeded random vector. Return `(lam, v)` with `v` the final unit vector and `lam` the Rayleigh quotient $v^\top A v / v^\top v$ for $A$ itself.
- `all_by_shifts(A, guesses)`: the sorted list of eigenvalues found from the given guesses, one per guess, rounded to 10 decimals and without repeats.

## Hints

1. `np.linalg.solve(A - mu * np.eye(n), x)`.
2. A guess equal to an eigenvalue makes the system singular; guesses in the tests are close but not equal.
3. Rounding before `sorted(set(...))` merges eigenvalues found twice.
