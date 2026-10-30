# Products of probabilities underflow

- `likelihood_product(ps)`: the product of the probabilities, multiplied in order as float64.
- `log_likelihood_naive(ps)`: `np.log` of that product (it becomes $-\infty$ when the product underflows to 0).
- `log_likelihood(ps)`: the sum of the logs, which never underflows.
- `underflow_length(p)`: the smallest number $n$ of factors equal to `p` whose product is exactly 0 in float64. Multiply step by step until it hits 0.

## Hints

1. `float(np.prod(np.asarray(ps)))`.
2. Wrap `np.log` of zero in `np.errstate(divide="ignore")`.
3. `float(np.sum(np.log(ps)))`.
