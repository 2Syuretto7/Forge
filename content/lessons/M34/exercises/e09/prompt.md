# Reading a weight matrix by its spectrum

A trained weight matrix is not random, and its spectrum shows it: random initialization leaves a Marchenko-Pastur bulk, and what training learned shows up as eigenvalues outside it (Section 7). Here a "trained" matrix is simulated as noise plus a few planted directions, so you know the right answer.

- `top_eigenvalue(S)` and `grad_top_eigenvalue(S)`: for a symmetric $S$, $\lambda_{\max}$ and its gradient with respect to the entries, $vv^\top$ for the top unit eigenvector $v$ when $\lambda_{\max}$ is simple.
- `count_outliers(W, margin=1.05)`: for $W$ of shape $n \times p$ with noise of variance 1 per entry, the number of eigenvalues of $W^\top W/n$ above `margin` times the edge $(1 + \sqrt{p/n})^2$.
- `planted_matrix(n, p, strengths, rng)` is provided: noise plus one rank-one term per strength.

The tests run a **gradient check** with a symmetric perturbation, then count the planted directions that rise above the edge and miss those below the BBP threshold.

## Hints

1. Perturbing $S$ by a symmetric $E$ changes $\lambda_{\max}$ by $v^\top Ev$ to first order, which is $\sum_{ij}E_{ij}v_iv_j$.
2. A planted strength is detectable only above the threshold of e08; weaker ones are real but invisible.
3. Real trained layers also show heavy tails in their singular values, a sign of correlations that pure noise never has.
