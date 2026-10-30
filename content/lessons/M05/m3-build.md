# Build: sequences, exact sums, an induction checker and loop counters

Python's `fractions.Fraction` stores rationals exactly: `Fraction(1, 3) + Fraction(1, 6) == Fraction(1, 2)` with no rounding. Exact arithmetic lets you check formulas with no doubt about rounding, which is what the build movement of a lesson about proof should do.

## Sequences and sums

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

:::exercise{ref=e03}
:::

:::exercise{ref=e04}
:::

## Limits

:::exercise{ref=e05}
:::

## Induction, checked symbolically

A formula for $\sum_{k=1}^n f(k)$ is a polynomial $F(n)$. Induction's step is "$F(n + 1) - F(n) = f(n + 1)$ for every $n$", and for polynomials you can check that for every $n$ at once by comparing coefficients.

:::exercise{ref=e06}
:::

## Counting the cost of loops

:::exercise{ref=e07}
:::

:::exercise{ref=e08}
:::

:::exercise{ref=e09}
:::
