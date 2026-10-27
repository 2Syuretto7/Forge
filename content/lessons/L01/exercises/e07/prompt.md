# Power iteration and its convergence rate

Implement the top eigenpair of a symmetric matrix by repeated multiplication (Section 5).

- `power_iteration(S, iters, seed)`: start from `x = np.random.default_rng(seed).normal(size=n)`, repeat `iters` times `x = S @ x; x = x / norm(x)`, then return `(lam, v)` where `v` is the final unit vector, flipped so that its largest-magnitude entry is positive, and `lam` is the Rayleigh quotient $v^\top S v$.
- `gap_ratio(S)`: return $|\lambda_2| / |\lambda_1|$, the two largest eigenvalues in absolute value (`np.linalg.eigvalsh` is allowed here).
- `iterations_needed(ratio, tol)`: the smallest integer $k$ with $\text{ratio}^k \le \text{tol}$.

One test runs your iteration for 20 and 40 steps and checks that the error shrinks by about $(\lambda_2/\lambda_1)^{20}$, as derived.

## Hints

1. Use the given seed exactly as described so the test can reproduce your starting vector.
2. `i = np.argmax(np.abs(v)); v = v * np.sign(v[i])` fixes the sign.
3. $k = \lceil \ln(\text{tol}) / \ln(\text{ratio}) \rceil$; `math.ceil` returns an int.
