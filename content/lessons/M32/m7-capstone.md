# Capstone: a sampler you can defend

Sample the posterior of a two-parameter logistic regression with a Markov chain of your own design, and back the result with diagnostics: the acceptance rate, traces, autocorrelations, effective sample sizes and $\hat R$. The tests compare your means and standard deviations with a brute-force integral of the posterior over a grid, to within your own Monte Carlo standard errors.

:::exercise{ref=capstone}
:::

## When you finish

You can build a chain for any target you can evaluate up to a constant, and say how far to trust what it reports. M37 runs a Langevin-type chain from noise to data in diffusion models; M29's noise floor reads differently now that you know it is a stationary distribution.

:::edge{to=M37 text="diffusion models and the reverse of a noising chain."}
:::

:::edge{to=M29 text="the noise floor of constant-step SGD as a stationary distribution."}
:::
