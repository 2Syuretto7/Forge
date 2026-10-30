# The prime race

Every odd prime leaves remainder 1 or 3 when divided by 4. Count them up to $n$.

- `sieve(n)`: the list of primes up to and including `n`, by the sieve of Eratosthenes: start with every number marked prime, and for each prime $p$ cross out $p^2, p^2 + p, \dots$.
- `race(n)`: the pair `(ones, threes)`: how many primes up to $n$ leave remainder 1, and how many leave remainder 3.
- `first_lead_change(limit)`: the smallest $n \leq$ `limit` at which the remainder-1 primes are strictly ahead, or `None`.

The claim "the remainder-3 primes are never behind" survives every test up to 26,860. Run your code and watch it fail at 26,861: that is how much evidence can mislead. (A proof that the lead changes infinitely often was given by J. E. Littlewood in 1914.)

## Hints

1. A list of booleans `is_p = [True] * (n + 1)` with `is_p[0] = is_p[1] = False`.
2. Walk $n$ upward once, updating both counts as you pass each prime, rather than calling `race` for every $n$.
3. `p % 4 == 1`.
