# The cost of a gradient

- `fd_evaluations(n)`: central differences, $2n$.
- `fd_seconds(n, eval_seconds)`: their time.
- `directional_evaluations(k)`: the random-direction check, $2k$.
- `analytic_ratio(cost_grad, cost_f)`: how many evaluations of `f` an analytic gradient costs, given the two costs.

Reverse-mode differentiation (M19) guarantees a gradient for a small constant times the cost of `f`, usually 2 to 4, whatever $n$ is.

## Hints

1. Plain arithmetic.
2. $2 \times 10^8$ evaluations of 1 ms is about 2.3 days.
3. `cost_grad / cost_f`.
