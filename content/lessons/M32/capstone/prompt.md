# Capstone: a sampler with its diagnostics

The starter's `make_data(seed=0)` returns 100 inputs $x_i$ and binary labels $y_i$ for a logistic regression with an intercept $a$ and a slope $b$: $P(y_i = 1) = \sigma(a + bx_i)$. With independent $N(0, 5^2)$ priors, sample the posterior of $\theta = (a, b)$ and report it with its diagnostics.

1. `log_post(theta)`: the log posterior up to a constant, for one parameter vector of shape `(2,)` (return a float) or a stack of shape `(m, 2)` (return `m` values). Use `np.logaddexp(0, z)` for $\log(1 + e^z)$.
2. `grad_log_post(theta)` for one vector.
3. `run_chains(n_chains=4, n=5000, seed=0)`: `(samples, acceptance)` with `samples` of shape `(n_chains, n, 2)`, after discarding a burn-in of your choice. Any correct sampler passes; a random walk whose proposal covariance is the inverse negative Hessian at the posterior mode, scaled by $2.38/\sqrt 2$, is fast and robust, especially with all chains updated together as one array.
4. `autocorr(x, max_lag)`, `ess(x)` and `r_hat(chains)` as in e08 and e15.
5. `diagnostics(samples)`: a dict with lists of length 2, one entry per parameter: `"mean"` and `"sd"` over all samples, `"ess"` (the sum of the chains' effective sample sizes), `"mcse"` (sd over the square root of ess), `"r_hat"`; and `"acf"`, an array of shape `(2, 51)` holding each parameter's autocorrelations at lags 0 to 50, averaged over chains.
6. `REPORT`: at least 120 words. Give the posterior means and standard deviations with their Monte Carlo errors; report the acceptance rate, the effective sample sizes and $\hat R$; describe what the trace and the autocorrelation show; and say how you would know if the sampler had failed.

The tests compute the posterior by brute-force numerical integration on a grid and require your means within 4 Monte Carlo standard errors of it, your standard deviations within 6 percent, $\hat R < 1.01$, and more than 1,000 effective samples for each parameter.
