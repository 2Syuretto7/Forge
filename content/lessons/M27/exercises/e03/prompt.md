# How small KL forces distributions together

A small KL divergence means the distributions are close in a strong sense. **Pinsker's inequality** makes that quantitative:

$$
\mathrm{TV}(p, q) \le \sqrt{\tfrac{1}{2}\,\mathrm{KL}(p\,\|\,q)}, \qquad \mathrm{TV}(p, q) = \tfrac12 \sum_x |p(x) - q(x)|,
$$

with KL in nats. Total variation is the largest difference in probability the two distributions can assign to any event.

- `total_variation(p, q)`.
- `pinsker_bound(p, q)`: the right-hand side.
- `worst_event(p, q)`: the event (as a boolean mask) that achieves the total variation: the outcomes where $p > q$.

## Hints

1. TV is half the L1 distance.
2. Reuse a KL implementation with the zero conventions.
3. $p(A) - q(A)$ for the mask $A = \{p > q\}$ equals the total variation.
