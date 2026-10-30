# Taylor approximators with error bounds

- `taylor_sin(x, terms)`: the sum of the first `terms` nonzero terms of $x - x^3/3! + x^5/5! - \dots$.
- `taylor_exp(x, terms)`: $\sum_{k < \text{terms}} x^k / k!$.
- `sin_bound(x, terms)`: the bound on the error of `taylor_sin`: the size of the first omitted term, $|x|^{2\,\text{terms}+1} / (2\,\text{terms}+1)!$.
- `terms_for(x, tol)`: the fewest terms for which `sin_bound` is below `tol`.

The tests check the bounds, and a **gradient check**: the derivative of the sine polynomial with $n$ terms, by central differences, equals the cosine polynomial (`taylor_cos`, provided) with $n$ terms.

## Hints

1. Build each term from the previous one: multiply by $-x^2 / ((2k)(2k + 1))$.
2. `math.factorial`.
3. `terms_for(0.1, 1e-10)` is 3, the puzzle's answer.
