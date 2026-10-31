# Detailed balance and the Metropolis matrix

A chain is **reversible** with respect to $\pi$ when $\pi_iP_{ij} = \pi_jP_{ji}$ for every pair: the flow from $i$ to $j$ equals the flow back. Summing over $i$ shows that $\pi$ is then stationary (Section 3). Metropolis-Hastings builds such a chain from any proposal matrix $Q$ (Section 5).

- `is_reversible(P, pi, tol=1e-12)`: whether every $\lvert\pi_iP_{ij} - \pi_jP_{ji}\rvert < $ `tol`.
- `metropolis_matrix(pi, Q)`: off the diagonal, $P_{ij} = Q_{ij}\min\left(1, \frac{\pi_jQ_{ji}}{\pi_iQ_{ij}}\right)$, and 0 where $Q_{ij} = 0$; the diagonal takes the rejected mass, $P_{ii} = 1 - \sum_{j \ne i}P_{ij}$.
- `cycle_chain(n, p)`: on a ring of $n$ states, move one step clockwise with probability $p$, otherwise stay.

The tests build Metropolis matrices from symmetric and asymmetric proposals, check detailed balance and stationarity, and show that the cycle chain has the uniform distribution as its stationary distribution without being reversible.

## Hints

1. The flow matrix is `pi[:, None] * P`; detailed balance says it is symmetric.
2. Build $P$ entry by entry off the diagonal, then set the diagonal from the row sums.
3. On the cycle, mass flows clockwise and never back, so the flow matrix cannot be symmetric.
