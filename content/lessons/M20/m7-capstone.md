# Capstone: a sampler toolkit

Five samplers turn uniform random numbers into other distributions: exponential, standard normal pairs by Box-Muller, uniform on the disc, Cauchy, and a correlated two-dimensional Gaussian. For each, write the map, its inverse and the target density, and verify the sampler twice: by a histogram of 200,000 samples against the density, and by the change-of-variables formula, computing $|\det J|$ of the inverse map numerically at many points and comparing it with the density.

:::exercise{ref=capstone}
:::

## When you finish

You can turn uniform noise into almost any distribution and prove that you did. M23 builds the multivariate Gaussian from the linear map $x = Lz$; M24 uses samplers for Monte Carlo; M37 sends whole distributions through learned invertible maps and noise-removal steps, where the Jacobian determinant is the bookkeeping.

:::edge{to=M37 text="density transport through learned maps: flows and diffusion."}
:::
