# Break it: a singularity, an oscillation, a jump

## Blowing up at an end

::::predict{id=p5 kind=choice answer=b}
The midpoint rule with $n$ strips on $\int_0^1 x^{-1/2}\,dx = 2$. How does the error shrink as $n$ grows?

- Like $1/n^2$, as for any midpoint rule.
- Like $1/\sqrt n$: the first strip alone, where the function is huge, carries an error that shrinks only that fast.
- It does not shrink: the integral is infinite.
- Like $1/n$.

:::reveal
Like $1/\sqrt n$. The error formula's $|f''|$ is infinite near 0, so the usual $h^2$ guarantee is void. The first strip, of width $1/n$, holds about $2/\sqrt n$ of the area, and the midpoint rule gets a constant fraction of it wrong. Substituting $x = t^2$ removes the singularity, $\int_0^1 2\,dt$, and the rules work again.
:::
::::

:::exercise{ref=e13}
:::

## Too few points for a fast oscillation

:::exercise{ref=e14}
:::

## A jump inside the interval

:::exercise{ref=e15}
:::

The integral test, in the widget: the harmonic sums grow like $\ln n$, as $\int_1^n dx/x$ does, while the sums of $1/k^2$ level off, as $\int_1^\infty dx/x^2 = 1$ does.

:::widget{name=SeriesStacker series=harmonic logn=4 logx=true}
:::

## What to take away

- Remove singularities by substitution before integrating numerically.
- Use several points per oscillation, or a method built for oscillatory integrands.
- Split the interval at known jumps and kinks; an error formula assumes smoothness.
