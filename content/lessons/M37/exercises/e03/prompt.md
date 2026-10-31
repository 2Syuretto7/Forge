# Ito's lemma, by summing

Ordinary calculus says $d(W^2) = 2W\,dW$. For Brownian motion it is wrong: $(dW)^2$ is of size $dt$, not negligible, and **Ito's lemma** adds it back, $d(W^2) = 2W\,dW + dt$ (Section 3). Check it by summing over a fine grid: the left-point sum $\sum_kW_{t_k}(W_{t_{k+1}} - W_{t_k})$ approaches $\frac12(W_T^2 - T)$, while the midpoint-averaged sum $\sum_k\frac12(W_{t_k} + W_{t_{k+1}})(W_{t_{k+1}} - W_{t_k})$ equals $\frac12W_T^2$ exactly, the ordinary-calculus answer.

- `ito_sum(W)`: the left-point sum along one path.
- `midpoint_sum(W)`: the averaged sum.
- `quadratic_variation(W)`: $\sum_k(W_{t_{k+1}} - W_{t_k})^2$, which tends to $T$.

The tests run a fine path to $T = 1$ and check all three.

## Hints

1. `np.diff(W)` gives the increments; `W[:-1]` the left endpoints.
2. The difference between the two sums is half the quadratic variation.
3. The left-point (Ito) convention is the one Euler-Maruyama uses: the coefficients are evaluated before the step, without looking ahead.
