# How often is a system nearly singular, and how much does it hurt?

- `fraction_small_det(n, t, seed=0)`: draw `n` random $2 \times 2$ matrices with entries uniform in $[-1, 1]$ (use `np.random.default_rng(seed).uniform(-1, 1, size=(n, 2, 2))`) and return the fraction whose determinant is smaller than `t` in absolute value.
- `amplification(A, b, eps=1e-6)`: how much a small change in the right-hand side moves the solution of $Ax = b$. Solve the system, then solve it again with `b` nudged by `eps` in each of the four directions $(\pm \text{eps}, 0)$ and $(0, \pm \text{eps})$; return the largest distance the solution moved divided by `eps`.

Use `np.linalg.solve(A, b)` for single systems and `np.linalg.norm(v)` for the length of a vector.

## Hints

1. Reuse the vectorized determinant formula, then `np.mean(np.abs(det) < t)`.
2. Build the four nudges as `[np.array([eps, 0]), np.array([-eps, 0]), ...]`.
3. A well-behaved system has amplification around 1; a nearly singular one, far more.
