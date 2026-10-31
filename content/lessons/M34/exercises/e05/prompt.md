# Proving the lemma: a chi-square tail

Fix one difference vector $x$. Then $k\lVert R^\top x\rVert^2/\lVert x\rVert^2$ is a sum of $k$ squared standard normals, a $\chi^2_k$ variable, whose log moment generating function is $\log\mathbb{E}e^{tZ} = -\frac k2\log(1 - 2t)$ for $t < \frac12$ (Section 4). Markov's inequality on $e^{tZ}$, optimized over $t$, gives the upper tail

$$
P\big(Z \ge (1 + \varepsilon)k\big) \le \big((1 + \varepsilon)e^{-\varepsilon}\big)^{k/2} \le e^{-\frac k2(\varepsilon^2/2 - \varepsilon^3/3)} ,
$$

and a union bound over the $\binom n2$ pairs finishes the proof.

- `log_mgf_chi2(t, k)` and `d_log_mgf_chi2(t, k)` $= \frac k{1 - 2t}$.
- `chernoff_upper(k, eps)`: $((1 + \varepsilon)e^{-\varepsilon})^{k/2}$.
- `simple_upper(k, eps)`: $e^{-\frac k2(\varepsilon^2/2 - \varepsilon^3/3)}$.
- `empirical_upper(k, eps, trials, rng)`: the fraction of simulated $\chi^2_k$ draws at or above $(1 + \varepsilon)k$.
- `union_failure(n, k, eps)`: $\binom n2\cdot 2\cdot$ `simple_upper(k, eps)`, the bound on the chance that some pair fails either way.

The tests run a **gradient check**, confirm the chain empirical $\le$ Chernoff $\le$ simple, and that the lemma's $k$ makes the union bound below 1.

## Hints

1. Setting the derivative of $t(1 + \varepsilon)k - \log\mathbb{E}e^{tZ}$ to zero gives $t = \frac{\varepsilon}{2(1 + \varepsilon)}$.
2. $\log(1 + \varepsilon) \le \varepsilon - \varepsilon^2/2 + \varepsilon^3/3$ turns the Chernoff bound into the simple one.
3. `rng.chisquare(k, trials)` draws the variable directly.
