# The probability-flow ODE

The reverse SDE is not the only way back. The ordinary differential equation (Section 7)

$$
\frac{dx}{dt} = -x - \nabla\log p_t(x)
$$

moves samples so that their distribution at each time is exactly $p_t$, the same marginals as the SDE, with no noise at all. It is a deterministic, invertible map from noise to data, and densities change along it by the change-of-variables rule of M20. Integrate it backwards from $T$ to near 0.

- `flow_backward(score, x, T, steps, tmin=1e-3)`: Euler steps $x \leftarrow x + h(x + \nabla\log p_t(x))$ on e07's geometric grid.
- `flow_forward(score, x, T, steps, tmin=1e-3)`: the reverse traversal, $x \leftarrow x - h(x + \nabla\log p_t(x))$ from `tmin` up to $T$, using the score at the later time of each step, so that it undoes `flow_backward` up to the step error.
- `w1(x, y)` as in e07.

The tests map noise to data with the exact score, then map the generated data forward again and recover the noise to within a small error.

## Hints

1. Reuse e07's grid; walk it in the opposite order for the forward map.
2. The ODE has half the score term of the SDE and no noise: the noise of the SDE does, on average, the other half of the work.
3. Deterministic sampling lets you encode data into noise and back, and compute likelihoods; stochastic sampling corrects its own errors better.
