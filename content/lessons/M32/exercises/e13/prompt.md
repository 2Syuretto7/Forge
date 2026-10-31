# Break it: chains that never forget where they started

The convergence theorem needs two conditions (Section 2). **Irreducible**: every state can reach every other. **Aperiodic**: returns to a state are not locked to multiples of some period greater than 1. Break each and watch the conclusions fail.

- `communicating_classes(P)`: the sets of states that can reach each other, as a sorted list of sorted lists. State $j$ is reachable from $i$ if some power of $P$ has $(P^t)_{ij} > 0$, with $t = 0$ allowed.
- `n_stationary(P, tol=1e-9)`: the number of eigenvalues within `tol` of 1, which counts the independent stationary distributions.
- `period(P, i)`: the greatest common divisor of the return times $t \le 3n$ with $(P^t)_{ii} > 0$.
- `long_run(P, x0, steps=2000)`: the distribution $e_{x_0}P^{\text{steps}}$.

The tests use a chain made of two separate blocks, where the long run depends on the starting state and there are two stationary distributions, and a deterministic three-cycle, which has period 3 and never converges, until it is made lazy.

## Hints

1. Reachability: repeat `R = R | (R @ A > 0)` with `A = P > 0` and `R` starting as the identity until nothing changes.
2. States $i$ and $j$ communicate when `R[i, j] and R[j, i]`.
3. `math.gcd` folds over a list with `functools.reduce`.
