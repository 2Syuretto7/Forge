# Recall bridge: from fixed data to chosen actions

M24 estimated expectations by averaging samples; M27 differentiated the log-likelihood of a softmax; M29 descended along noisy gradients. Here the samples are the model's own actions, and the quantity to improve is the expected reward of those actions. Nothing can be differentiated through a sampled token, yet the gradient exists, and Monte Carlo can estimate it. Clear your due cards above first.

:::edge{from=M24 text="Monte Carlo returns as gradient estimation"}
:::

:::edge{from=M27 text="the softmax, its score and the KL divergence"}
:::

:::edge{from=M29 text="stochastic gradients and their noise"}
:::

## What carries over

Monte Carlo averages and their variance $\sigma^2/n$ (M24); the softmax, the gradient of $\log\mathrm{softmax}$, which is one-hot minus probabilities, and the KL divergence (M27); stochastic gradient steps (M29); Markov chains and their transition matrices (M32); and the Gibbs form $\pi \propto \pi_{\text{ref}}e^{r/\beta}$ of a KL-regularized optimum (M30).
