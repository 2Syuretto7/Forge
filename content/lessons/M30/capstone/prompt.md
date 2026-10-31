# Capstone: a dual SVM solver and the KL-regularized optimum

Part 1. Solve the soft-margin SVM through its dual by coordinate ascent (e06) on the starter's `make_data()` (400 points in 5 dimensions, with a constant feature for the bias), to a **KKT residual below $10^{-4}$**:

1. `solve(X, y, C, tol=1e-5, max_epochs=500, seed=0)`: sweep the coordinates in random order until the KKT residual is at most `tol`; return `(alpha, w)`.
2. `kkt_residual(alpha, X, y, C)`: the largest projected-gradient violation. With $G_i = y_i w^\top x_i - 1$: $\lvert G_i\rvert$ if $0 < \alpha_i < C$, $\max(0, -G_i)$ if $\alpha_i = 0$, and $\max(0, G_i)$ if $\alpha_i = C$.
3. `duality_gap(alpha, X, y, C)`: $P(w) - D(\alpha)$, relative to $P(w)$.

Part 2. For a reference distribution $\pi$ and rewards $r$:

4. `kl_optimum(pi, r, beta)`: the maximizer of $\sum p_i r_i - \beta\,\mathrm{KL}(p\,\|\,\pi)$, which Section 6 derives as $\pi_i e^{r_i/\beta}/Z$.
5. `check_kl_optimum(pi, r, beta, trials, rng)`: the largest amount by which any of `trials` random distributions beats `kl_optimum` on the objective (at most 0 when the formula is right).
6. `log_ratio_slope(pi, r, beta)`: the least-squares slope of $\log(p_i/\pi_i)$ against $r_i$, which must equal $1/\beta$.

The tests require the KKT residual below $10^{-4}$, a relative duality gap below $10^{-5}$, the slackness categories of e07 all consistent, and the KL optimum unbeaten by 1,000 random distributions with the slope $1/\beta$.
