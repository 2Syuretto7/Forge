# Recall bridge: numbers a computer can hold

M06 built exponentials and logarithms, and M15 met the first sign of trouble: a finite difference with a tiny step returns garbage, because the computer's numbers are not the real numbers. This lesson opens the box: what a floating-point number is, how every operation rounds, which formulas amplify those roundings into nonsense, and how the functions inside every training loop are written to survive. Clear your due cards above first.

:::edge{from=M06 text="exponentials and logarithms"}
:::

:::edge{from=M15 text="finite differences and their rounding error"}
:::

## What carries over

The exponential grows faster than any number format can follow, the logarithm undoes it, and M15's best finite-difference step, about $10^{-8}$, balances truncation against rounding.
