# Break it: temperature to zero and to infinity

The Gibbs distribution $p_i \propto e^{r_i/\tau}$ written as `np.exp(r / tau) / np.sum(np.exp(r / tau))` overflows to `inf / inf = nan` as soon as $r/\tau$ passes about 709, and at very high temperatures every probability rounds to the same value.

- `naive_gibbs(r, tau)`: the formula as written, under `np.errstate(all="ignore")`.
- `stable_gibbs(r, tau)`: with the maximum subtracted.
- `limit_low(r)`: the $\tau \to 0$ limit, uniform over the actions that share the maximum reward.
- `limit_high(r)`: the $\tau \to \infty$ limit, uniform.

The tests find the naive version returning `nan` at $\tau = 10^{-3}$ for rewards of order 1, the stable version matching both limits, and a tie at the top split evenly.

## Hints

1. `np.isclose(r, r.max())` marks the best actions.
2. Subtracting the maximum makes the largest exponent 0, so the sum is at least 1.
3. At $\tau = 10^{12}$ every exponent rounds to $e^0$: the stable version returns the uniform distribution, correctly.
