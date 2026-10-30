# No fraction is the square root of 2

The proof by contradiction says $p^2 = 2q^2$ has no solution in positive integers. So $p^2 - 2q^2$ is never 0, and since it is an integer it is at least 1 in absolute value. That gives a concrete, checkable consequence: no fraction gets closer to $\sqrt{2}$ than a certain distance.

- `gap(p, q)`: the integer $|p^2 - 2q^2|$.
- `best_fraction(q)`: the integer $p$ that makes $p/q$ closest to $\sqrt{2}$, as the pair `(p, q)`.
- `smallest_gap(max_q)`: the smallest `gap(p, q)` over $q = 1, \dots,$ `max_q` with $p$ from `best_fraction(q)`. The theorem predicts it is never 0; the tests also discover that 1 is reached infinitely often.
- `closest_fractions(max_q)`: the list of `(p, q)` with gap exactly 1, in increasing $q$ (these are the best rational approximations of $\sqrt{2}$: 1/1, 3/2, 7/5, 17/12, ...).

## Hints

1. `round(q * 2 ** 0.5)` gives the best $p$.
2. Loop over `q` and keep the smallest gap.
3. Collect the fractions whose gap equals 1.
