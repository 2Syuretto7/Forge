# Bisection

- `bisect(f, a, b, tol=1e-12, max_iter=200)`: for continuous `f` with $f(a)$ and $f(b)$ of opposite signs, repeatedly halve the bracket, keeping the half where the sign changes, until it is shorter than `tol`. Return `(root, iterations)` with `root` the midpoint of the final bracket. Raise `ValueError` if the signs at the ends do not differ.
- `predicted_iterations(a, b, tol)`: $\lceil \log_2((b - a)/\text{tol}) \rceil$.

## Hints

1. Compare signs with `f(a) * f(m) <= 0`, or better `(f(a) < 0) != (f(m) < 0)` to avoid overflow.
2. An exact zero at the midpoint can end the loop early.
3. The number of steps depends only on the bracket and the tolerance, not on `f`.
