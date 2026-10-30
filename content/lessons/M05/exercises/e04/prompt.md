# Closed forms

Write each sum in closed form (no loops), as integers:

- `sum_first(n)` $= 1 + 2 + \dots + n$;
- `sum_odds(n)` $= 1 + 3 + \dots + (2n - 1)$;
- `sum_squares(n)` $= 1^2 + \dots + n^2 = \dfrac{n(n + 1)(2n + 1)}{6}$;
- `sum_cubes(n)` $= 1^3 + \dots + n^3$, which is the square of `sum_first(n)` (a surprising identity; the tests check it against brute force).

Use integer division `//`: each numerator is divisible by its denominator, so the result is exact.

## Hints

1. `n * (n + 1) // 2`.
2. The sum of the first $n$ odd numbers is $n^2$.
3. `sum_first(n) ** 2`.
