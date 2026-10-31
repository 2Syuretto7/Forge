# Capstone: honest error bars

Build a small Monte Carlo engine: integrals, expectations and rare-event probabilities, each reported with a 95 percent interval. Then test the intervals the way a statistician would: rerun each estimate 100 times with fresh random numbers and count how often the interval contains the truth. At least 93 of 100 must.

:::exercise{ref=capstone}
:::

## When you finish

You can turn any expectation into a computation with an error bar, and you know the three ways that error bar can lie. M25 asks the reverse question, from data to the parameters that produced them; M29 averages noisy gradients; M31 sharpens Chebyshev's bound into exponential ones.

:::edge{to=M29 text="stochastic gradients are Monte Carlo estimates of the full gradient."}
:::

:::edge{to=M26 text="summing a million samples needs compensated summation."}
:::
