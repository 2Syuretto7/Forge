# The birthday problem

- `p_shared(m, days=365)`: the exact probability that some two of `m` people share a birthday, as a float, from the product $\prod_{i=0}^{m-1} \frac{\text{days} - i}{\text{days}}$.
- `p_shared_approx(m, days=365)`: the approximation $1 - e^{-m(m-1)/(2\,\text{days})}$.
- `smallest_room(target, days=365)`: the smallest $m$ with `p_shared(m) >= target`.
- `simulate_room(m, n, seed=0)`: the fraction of `n` simulated rooms of `m` people (birthdays from `random.Random(seed).randrange(365)`) with a shared birthday.

## Hints

1. Multiply in a loop, then subtract from 1.
2. `math.exp(-m * (m - 1) / (2 * days))`.
3. A room has a match when `len(set(birthdays)) < m`.
