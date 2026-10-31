# Recall bridge: from random walks to generative models

M32 turned a random walk into Brownian motion and used Langevin dynamics to sample a fixed target; M23 conditioned Gaussians; M20 transported densities through invertible maps. A diffusion model combines all three: it destroys data with a Gaussian noising process, learns how the density changes along the way, and runs the process backwards to create new data. Clear your due cards above first.

:::edge{from=M32 text="Brownian motion and Langevin dynamics"}
:::

:::edge{from=M23 text="Gaussian conditionals"}
:::

:::edge{from=M20 text="change of variables returns as density transport in diffusion"}
:::

## What carries over

Brownian motion as the limit of a scaled random walk, with independent $N(0, h)$ increments, and the Langevin diffusion $dX = \nabla\log\pi\,dt + \sqrt2\,dW$ that samples $\pi$ (M32); the Gaussian conditional and its mean and covariance (M23); how a density changes under an invertible map (M20); and the regression fact that a conditional expectation minimizes squared error (M22).
