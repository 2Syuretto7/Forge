# Capstone: an adaptive quadrature library

Build `integrate(spec)`: adaptive Simpson underneath, a change of variables for infinite intervals, another for integrands that blow up at the left end, and a count of evaluations. Twenty integrals with known values test it, from polynomials to the Gaussian over the whole line, a Beta normalizer, logarithmic singularities and a kink; every one must come out within $10^{-8}$.

:::exercise{ref=capstone}
:::

## When you finish

You can compute nearly any one-dimensional integral to eight digits and say how much it cost. M20 integrates over the plane and changes variables there; M22 computes expectations as integrals against densities; M24 replaces your grids by random samples, the only approach that survives in a hundred dimensions.

:::edge{to=M20 text="multiple integrals and the change-of-variables formula."}
:::
