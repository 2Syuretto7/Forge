# Recall bridge: averages, logs and counting

This lesson has no prerequisite lessons, so the bridge checks three tools from school mathematics that probability leans on: averages, logarithms and counting. If L01 is complete and any of its items are due, they appear above.

## Averages

The average of $x_1, \dots, x_n$ is $\bar x = \frac{1}{n}\sum_i x_i$. A **weighted** average uses weights $w_i \ge 0$ that sum to one: $\sum_i w_i x_i$. An expectation is a weighted average where the weights are probabilities.

## Logarithms turn products into sums

Likelihoods are products of many probabilities, and products of many numbers below one underflow to zero in floating point. Logarithms fix both the algebra and the numerics: $\log(ab) = \log a + \log b$, and $\log$ is increasing, so maximizing $\log f$ and maximizing $f$ pick the same point.

## Counting

The number of ways to choose $k$ items out of $n$ is $\binom{n}{k} = \dfrac{n!}{k!\,(n-k)!}$. It counts the orderings of heads and tails that contain exactly $k$ heads.

::::derivation{id=d0 title="Warm-up"}
:::step
The weighted average of the values $0$ and $10$ with weights $0.7$ and $0.3$ is [[3]].
:::
:::step
$\log(2 \cdot 3 \cdot 5) = \log 2 + \log 3 + \log 5$. The derivative of $\log x$ is [[1/x]].
:::
:::step
The number of sequences of 4 coin flips with exactly 2 heads is $\binom{4}{2} =$ [[6]].
:::
:::step
If each flip lands heads with probability $p$, one particular sequence with 2 heads and 2 tails has probability $p^2(1-p)^2$. So the probability of exactly 2 heads in 4 flips is [[6*p^2*(1-p)^2]].
:::
::::

That last expression, read as a function of $p$ with the data fixed, is the likelihood. It is the central object of this lesson.
