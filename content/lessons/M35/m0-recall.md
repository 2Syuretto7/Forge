# Recall bridge: from one fit to a forecast

M25 fitted models by least squares and maximum likelihood and put intervals on the estimates with standard errors and the bootstrap; M29 proved how fast gradient methods converge and why conditioning matters; M01 read numbers by their orders of magnitude. This lesson combines them for the most consequential fit in modern machine learning: a power law fitted to small training runs and extrapolated to a run a hundred times larger. Clear your due cards above first.

:::edge{from=M25 text="least squares, standard errors and the bootstrap"}
:::

:::edge{from=M29 text="Newton-type steps and conditioning"}
:::

:::edge{from=M01 text="orders of magnitude return as compute budgets on log-log axes"}
:::

## What carries over

Least squares as maximum likelihood under Gaussian noise, the standard error $s\sqrt{(X^\top X)^{-1}_{jj}}$, and the percentile bootstrap (M25); Newton's method and the effect of conditioning on iterative solvers (M29, M33); and logarithms as the scale on which multiplicative changes become additive (M01).
