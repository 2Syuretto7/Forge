# Scale: the unit ball from 2 to 50 dimensions

Compute $V_n$ by the formula, and estimate the fraction of the cube $[-1, 1]^n$ inside the ball by sampling, for $n$ from 2 to 50.

::::predict{id=p4 kind=choice answer=d}
A million uniform points in the cube $[-1, 1]^{20}$. About what fraction lands inside the unit ball?

- About half.
- About 5 percent.
- About one in ten thousand.
- About $2.5 \times 10^{-8}$: almost certainly none of the million.

:::reveal
$V_{20}/2^{20} = \frac{\pi^{10}}{10!\,2^{20}} \approx 2.5 \times 10^{-8}$. Almost all of a high-dimensional cube's volume sits in its corners, far from the centre. Rejection sampling from a cube is hopeless in high dimension, and grid-based integration is worse; sampling directly from the target, as the change of variables lets you do, is the way out.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
