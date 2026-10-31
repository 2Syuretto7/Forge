# Brownian motion and Euler-Maruyama

A stochastic differential equation $dX = a(X, t)\,dt + b(X, t)\,dW$ adds to an ordinary differential equation a random kick from Brownian motion, whose increments over a step $h$ are independent $N(0, h)$ (Section 1, M32). The **Euler-Maruyama** method steps it forward: $X_{k+1} = X_k + a(X_k, t_k)h + b(X_k, t_k)\sqrt h\,z_k$ with standard normal $z_k$.

- `brownian_paths(n_paths, T, steps, rng)`: an array of shape `(n_paths, steps + 1)`, starting at 0.
- `euler_maruyama(a, b, x0, T, steps, n_paths, rng)`: the final values $X_T$ of `n_paths` paths, with `a(x, t)` and `b(x, t)` vectorized over paths.

The tests check that $\operatorname{Var}W_T = T$ with independent increments, and that geometric Brownian motion, $dX = \mu X\,dt + \sigma X\,dW$, has $\mathbb{E}X_T = x_0e^{\mu T}$.

## Hints

1. `np.cumsum` of scaled normal increments, with a column of zeros in front.
2. The noise term scales with $\sqrt h$, not $h$: Brownian motion moves a distance $\sqrt h$ in time $h$.
3. Vectorize across paths and loop over steps.
