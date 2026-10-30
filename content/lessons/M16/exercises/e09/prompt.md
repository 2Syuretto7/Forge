# Measuring convergence

- `errors(history, root)`: $|x_k - r|$ for each iterate.
- `orders(errs)`: the estimates $p_k = \ln(e_{k+1}/e_k) / \ln(e_k/e_{k-1})$ from consecutive triples of errors between $10^{-14}$ and $10^{-1}$.
- `rates(errs)`: the ratios $e_{k+1}/e_k$ over the same range.
- `classify(errs)`: `"linear"` if the last order estimate is below 1.25, `"quadratic"` if above 1.8, otherwise `"superlinear"`.

## Hints

1. Filter first, then form ratios.
2. A linear method has constant ratios, so its order estimates are near 1.
3. With fewer than three usable errors, return an empty list of orders.
