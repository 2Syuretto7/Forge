# Power iteration and its rate

- `power_iteration(S, iters, seed=0)`: start from `x = np.random.default_rng(seed).normal(size=n)`, repeat `iters` times `x = S @ x; x = x / norm(x)`, and return `(lam, v)`: `v` the final unit vector, flipped so that its largest-magnitude entry is positive, and `lam` the Rayleigh quotient $v^\top S v$.
- `gap_ratio(S)`: $|\lambda_2| / |\lambda_1|$ for the two eigenvalues largest in absolute value (`np.linalg.eigvalsh` is allowed here).
- `iterations_needed(ratio, tol)`: the smallest integer $k$ with $\text{ratio}^k \leq \text{tol}$.

One test runs your iteration for 20 and 40 steps and checks that the error shrinks by about $(\lambda_2/\lambda_1)^{20}$.

## Hints

1. Use the seed exactly as described so the test can reproduce your start.
2. `i = np.argmax(np.abs(v)); v = v * np.sign(v[i])`.
3. $k = \lceil \ln(\text{tol}) / \ln(\text{ratio}) \rceil$.
