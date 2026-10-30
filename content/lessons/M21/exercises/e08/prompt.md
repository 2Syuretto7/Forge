# Pairwise is not mutual

Toss two fair coins $A$ and $B$, and let $C$ be "they agree".

- `space()`: the four outcomes `(a, b)` with probability $\frac14$.
- `events()`: the three events $A$ = first coin heads, $B$ = second heads, $C$ = the coins agree, as sets.
- `pairwise_independent(space, events)`: whether each pair is independent.
- `mutually_independent(space, events)`: whether also $P(A \cap B \cap C) = P(A)P(B)P(C)$.

Every pair is independent, yet knowing any two determines the third: independence of each pair does not make the three independent.

## Hints

1. Encode heads as 1.
2. Use $P(X \cap Y) = P(X)P(Y)$ for each of the three pairs.
3. $P(A \cap B \cap C) = \frac14$ but the product is $\frac18$.
