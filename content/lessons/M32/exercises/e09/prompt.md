# From random walk to Brownian motion

Take a $\pm 1$ random walk $S_k$ and squeeze it: $n$ steps per unit of time, each scaled by $1/\sqrt n$, so $W(k/n) = S_k/\sqrt n$. By the central limit theorem $W(t)$ is close to $N(0, t)$, and increments over disjoint intervals are independent: in the limit, Brownian motion (Section 8). Its density $p(x, t) = \frac{1}{\sqrt{2\pi t}}e^{-x^2/(2t)}$ solves the heat equation $\partial_tp = \frac12\partial_x^2p$.

- `scaled_walk(n, T, paths, rng)`: `(times, W)` with `times` the $nT + 1$ values $k/n$ and `W` of shape `(paths, nT + 1)`, starting at 0.
- `heat_kernel(x, t)`, `d_heat_dx(x, t)`, `d2_heat_dx2(x, t)`, `d_heat_dt(x, t)`: the density and its derivatives, in closed form.

The tests run a **gradient check** of your derivatives by finite differences, confirm the heat equation, and check that the scaled walk has variance $t$, uncorrelated increments, and the heat kernel as the histogram of $W(1)$.

## Hints

1. $\partial_xp = -\frac xt\,p$; differentiate once more with the product rule.
2. $\partial_tp = \left(\frac{x^2}{2t^2} - \frac1{2t}\right)p$.
3. Build the walk with `np.cumsum` of a matrix of signs, and prepend a column of zeros.
