# Recall bridge: the whole track at once

Thirty-seven lessons built tools one at a time. A real paper uses many of them in a single page, without saying which. This lesson takes three papers that changed how models are trained, DPO, LoRA and Adam, and derives every equation in them from the lessons you have done, reproduces each central claim in NumPy, and breaks each by removing one assumption. Clear your due cards above first.

:::edge{from=M30 text="the Gibbs optimum of a KL-regularized objective"}
:::

:::edge{from=M36 text="policy gradients and optimizing a proxy reward"}
:::

:::edge{from=M33 text="low-rank structure and the cost of matrix products"}
:::

:::edge{from=M35 text="fitting, uncertainty and checking a claim against data"}
:::

## What carries over

The KL divergence and cross-entropy (M27); the Gibbs form $\pi \propto \pi_{\text{ref}}e^{r/\beta}$ (M30); REINFORCE and the KL-regularized objective (M36); the SVD and Eckart-Young (M14); backpropagation through a product of matrices (M19); exponential averages, geometric series and the convergence of gradient methods (M05, M29); and the habit, from every capstone, of checking a derivation by measurement.
