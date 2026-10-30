# Rearranging a series

The alternating harmonic series $1 - \frac{1}{2} + \frac{1}{3} - \dots$ converges to $\ln 2$. Rearrange its terms and the sum changes.

- `alternating(n)`: the sum of its first `n` terms, in the usual order.
- `one_up_two_down(blocks)`: the sum of `blocks` blocks of the rearrangement $\frac{1}{2j - 1} - \frac{1}{4j - 2} - \frac{1}{4j}$ for $j = 1, 2, \dots$ Every term of the original appears exactly once, in a different order. It converges to $\frac{1}{2}\ln 2$.
- `steer(target, n_terms)`: Riemann's construction. Keep two queues, the positive terms $1, \frac{1}{3}, \frac{1}{5}, \dots$ and the negative terms $-\frac{1}{2}, -\frac{1}{4}, \dots$ While the running sum is at most `target`, take the next positive term; otherwise take the next negative term. Return the sum after `n_terms` terms. It approaches any target you choose.

## Hints

1. `sum((-1) ** (k + 1) / k for k in range(1, n + 1))`.
2. Add the three terms of each block in a loop over `j`.
3. Keep two counters: the next odd denominator and the next even one.
