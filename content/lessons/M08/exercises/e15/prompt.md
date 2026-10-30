# Adding probabilities that overlap

- `p_six_in_rolls(n)`: the probability of at least one six in `n` rolls of a die, exactly, as a `Fraction` (complement rule).
- `p_by_adding(n)`: de Méré's reasoning, $n/6$, as a `Fraction`.
- `first_impossible()`: the smallest `n` for which `p_by_adding(n)` exceeds 1.
- `overcount(n)`: `p_by_adding(n) - p_six_in_rolls(n)`. By inclusion-exclusion it is the probability mass counted more than once: rolls with two or more sixes counted several times.
- `p_double_six(n)`: at least one double six in `n` rolls of two dice, $1 - (35/36)^n$. De Méré bet that 24 rolls would make a double six more likely than not, and lost money: check `p_double_six(24)`.

## Hints

1. `1 - Fraction(5, 6) ** n`.
2. `Fraction(n, 6)`.
3. The overcount is zero only for `n = 1`.
