# Explain it plainly: why the walk finds the target

Explain why a random walk with the right acceptance rule ends up sampling the right distribution.

Guidelines:

- Write 150 to 400 words.
- Use a target with a high region and a low region as the example.
- Say what the acceptance rule is balancing.
- Say what can go wrong in practice.

:::feynman{id=f1 prompt="Explain why a random walk with the right acceptance rule ends up sampling the right distribution." key_points="The walk is a Markov chain; if it can reach every region and is aperiodic, its distribution converges to its unique stationary distribution from any start|The acceptance rule makes the flow of probability from x to y equal to the flow from y to x when the chain is distributed as the target, which is detailed balance|Detailed balance makes the target stationary: a chain distributed as the target stays distributed as the target after one more step|The rule uses only the ratio of target densities, so the unknown normalizing constant cancels|Averages along the path converge to expectations under the target, with an error set by the autocorrelation through the effective sample size"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that detailed balance implies stationarity, and that the Metropolis-Hastings acceptance probability alpha(x, y) = min(1, pi(y) q(y, x) / (pi(x) q(x, y))) satisfies detailed balance." key_points="Sums pi_i P_ij = pi_j P_ji over i and uses that the rows of P sum to 1 to get sum_i pi_i P_ij = pi_j|Writes the transition from x to a different state y as q(x, y) alpha(x, y)|Shows that pi(x) q(x, y) alpha(x, y) = min(pi(x) q(x, y), pi(y) q(y, x)), which is symmetric in x and y|Notes that rejections only add to the probability of staying at x, which detailed balance does not constrain|Concludes that the target pi is a stationary distribution of the Metropolis-Hastings chain"}
:::
