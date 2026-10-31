# The maximum-entropy distribution with a given mean

Among distributions on $\{0, 1, \dots, K\}$ with mean $m$, which has the largest entropy? Lagrange multipliers for the two constraints, $\sum p_k = 1$ and $\sum k p_k = m$, give $\log p_k + 1 + \alpha + \beta k = 0$, so $p_k \propto e^{-\beta k}$: a truncated geometric (Gibbs) distribution (Section 6, and M27 for entropy).

- `gibbs(beta, K)`: the distribution $p_k \propto e^{-\beta k}$, computed stably.
- `mean_of(p)`: $\sum_k k p_k$.
- `max_entropy(m, K)`: find $\beta$ by bisection on $[-50, 50]$ (the mean decreases as $\beta$ grows) so that the mean is $m$, and return the distribution.
- `entropy(p)`: in nats.

The tests check the mean, and that random distributions with the same mean always have less entropy.

## Hints

1. Subtract the largest exponent before exponentiating, as in M26.
2. $m = K/2$ gives $\beta = 0$: the uniform distribution.
3. To make a random distribution with mean $m$, mix the maximum-entropy one with a random one of the same mean, or solve a small linear adjustment; the tests do this for you.
