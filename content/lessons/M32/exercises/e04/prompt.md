# Mixing time and the spectral gap

How far is the chain from stationary after $t$ steps? Measure the gap with the **total variation distance** $\lVert p - q\rVert_{TV} = \frac12\sum_i\lvert p_i - q_i\rvert$, the largest difference in probability the two distributions give any event (Section 4).

- `tv(p, q)`.
- `lazy_cycle(n)`: on a ring of $n$ states, stay with probability $\frac12$ and step to each neighbour with probability $\frac14$.
- `spectral_gap(P)`: $1 - \lvert\lambda_2\rvert$, where $\lvert\lambda_2\rvert$ is the second largest eigenvalue modulus.
- `mixing_time(P, eps=0.25)`: the smallest $t$ with $\max_x\lVert e_xP^t - \pi\rVert_{TV} \le \varepsilon$, the worst start; take $\pi$ from the eigenvector as in e02.

The tests check the lazy cycle's gap against $\frac12(1 - \cos(2\pi/n))$, find the mixing time growing like $n^2$, and confirm the distance shrinking by the factor $1 - \text{gap}$ per step in the long run.

## Hints

1. Keep the whole matrix $M = P^t$ and update it with `M = M @ P`; row $x$ is the distribution after $t$ steps from $x$.
2. Sort the eigenvalue moduli in decreasing order; the first is 1.
3. For the lazy cycle the eigenvalues are $\frac12 + \frac12\cos(2\pi k/n)$, all nonnegative, so laziness removes the periodicity of even rings.
