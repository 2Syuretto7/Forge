# Break it: the average of a function is not the function of the average

Linearity lets expectation pass through sums and constants, and nothing else. In general $\mathbb{E}[g(X)] \ne g(\mathbb{E}X)$, and the gap can decide an answer.

- `plug_in(g, values, probs)`: $g(\mathbb{E}X)$.
- `expect(g, values, probs)`: $\mathbb{E}[g(X)] = \sum_k g(x_k)\,p_k$.
- `mc_expect(g, samples)`: the Monte Carlo estimate, the average of $g$ over samples.
- `relu_second_moment()`: the exact $\mathbb{E}[\max(Z, 0)^2]$ for a standard normal $Z$. By symmetry it is half of $\mathbb{E}Z^2$.

The tests show $\mathbb{E}[1/X] \ne 1/\mathbb{E}X$, $\mathbb{E}X^2 - (\mathbb{E}X)^2 = \operatorname{Var}X$, the sign of the gap for convex $g$ (M28's Jensen inequality), and the ReLU factor of Section 6 by sampling.

## Hints

1. `g(np.sum(values * probs))` against `np.sum(g(values) * probs)`.
2. $\max(Z, 0)^2$ equals $Z^2$ for half the outcomes and 0 for the other half, by the symmetry of $Z$.
3. `np.mean(g(samples))`.
