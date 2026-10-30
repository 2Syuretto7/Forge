# Events on a finite space

A finite probability space is a dictionary from outcomes to probabilities that sum to 1; an event is a Python set of outcomes.

- `prob(space, A)`: $P(A)$.
- `conditional(space, A, B)`: $P(A \mid B)$; raise `ValueError` if $P(B) = 0$.
- `independent(space, A, B, tol=1e-12)`: whether $P(A \cap B) = P(A)P(B)$.
- `two_dice()`: the space of ordered pairs of fair dice, each with probability $1/36$.

## Hints

1. `sum(space[w] for w in A)`.
2. `A & B` is the intersection of two sets.
3. `{(i, j): 1 / 36 for i in range(1, 7) for j in range(1, 7)}`.
