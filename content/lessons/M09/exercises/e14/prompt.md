# The zero vector has no direction

- `naive_cosine(x, y)`: $x \cdot y / (\|x\|\,\|y\|)$ with NumPy, inside `np.errstate(all="ignore")` (a zero vector gives `nan`).
- `safe_cosine(x, y, eps=1e-12)`: raise `ValueError` if either vector has length below `eps`; otherwise the cosine.
- `normalize_rows_safe(X, eps=1e-12)`: normalize every row, leaving rows shorter than `eps` as zeros instead of producing `nan`, and also return the list of their indices: return `(U, bad)`.

The tests show that one zero row in a database spreads `nan` into every similarity computed with the naive version.

## Hints

1. `np.linalg.norm(x) < eps`.
2. Compute the norms, replace tiny ones by 1 for the division, then zero those rows.
3. `np.flatnonzero(norms < eps)`.
