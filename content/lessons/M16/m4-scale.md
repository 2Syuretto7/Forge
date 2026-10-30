# Scale: 100,000 root problems at once

A vectorized Newton iteration solves a whole array of equations in lockstep: one NumPy expression per step, every element updated together. The number of steps, not the number of problems, sets the time.

::::predict{id=p4 kind=numeric answer=50 tol=1}
Bisection starts with the bracket $[0, 1]$ and halves it each step. How many steps shrink it below $10^{-15}$?

:::reveal
50, since $2^{-50} \approx 8.9 \times 10^{-16}$. Newton's method, from a decent start, needs about 5 or 6 for the same accuracy: digits 1, 2, 4, 8, 16. Bisection's advantage is that it cannot fail on a continuous function with a sign change; Newton's is speed. Libraries combine them (Brent's method).
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
