# What pivoting saves

For the system $\varepsilon x_1 + x_2 = 1$, $x_1 + x_2 = 2$:

- `solve_both(eps)`: return `(x_naive, x_pivot)`, the solutions by elimination without row swaps and with the rows swapped first (the larger pivot), each as a NumPy array of 2 floats. Write the 2 by 2 elimination out by hand.
- `exact_x1(eps)`: the true $x_1 = 1 / (1 - \varepsilon)$.
- `digits(eps)`: for each method, the number of correct significant digits of $x_1$, $-\log_{10}$ of its relative error, capped at 16. Return `(naive_digits, pivot_digits)`.

For $\varepsilon = 10^{-8}$ the naive method keeps about 8 digits; for $10^{-20}$, none.

## Hints

1. Naive: multiplier $1/\varepsilon$, then $x_2 = (2 - 1/\varepsilon) / (1 - 1/\varepsilon)$ and $x_1 = (1 - x_2)/\varepsilon$.
2. Pivoted: multiplier $\varepsilon$, then $x_2 = (1 - 2\varepsilon) / (1 - \varepsilon)$ and $x_1 = 2 - x_2$.
3. A relative error of exactly 0 gives the cap of 16.
