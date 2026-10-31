# Transition matrices and simulated paths

A Markov chain on states $0, \dots, n - 1$ is a transition matrix $P$ with $P_{ij} = P(X_{t+1} = j \mid X_t = i)$: nonnegative entries, rows summing to 1 (Section 1). A distribution is a row vector, and one step multiplies it by $P$ on the right.

- `check_stochastic(P)`: `True` when $P$ is square, has no negative entries, and every row sums to 1 within $10^{-12}$.
- `distribution_after(pi0, P, n)`: $\pi_0 P^n$, by $n$ vector-matrix products.
- `simulate(P, x0, n, rng)`: a path of $n + 1$ states starting at `x0`, each next state drawn from the current row.

The tests use the weather chain of Section 1 (sunny stays sunny with probability 0.9; rainy turns sunny with probability 0.5) and check that a long path spends five sixths of its days sunny.

## Hints

1. Draw the next state by comparing one uniform number with the cumulative sums of the current row: `np.searchsorted(np.cumsum(row), u, side="right")`.
2. Rounding can leave the last cumulative sum a hair below 1; clip the index to $n - 1$.
3. Draw all the uniform numbers at once with `rng.random(n)` before the loop.
