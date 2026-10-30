# Break it: wrong order, no inverse, outside the domain

Composition, inversion and domains each fail in a characteristic way. Make each failure loud.

## The wrong order

A preprocessing pipeline that clips and then standardizes is a different machine from one that standardizes and then clips. Predict which outputs change before running it.

:::exercise{ref=e13}
:::

## Inverting what has no inverse

Inverting $f(x) = 3x + 2$ is solving the balance $3x + 2 = y$. The balance always levels at exactly one $x$, because the machine is one-to-one.

:::widget{name=BalanceScale a=3 b=2 c=0 d=11}
:::

For $x^2$ there are two inputs for every positive output, and bisection silently returns one of them, or none.

::::predict{id=p5 kind=choice answer=c}
You run bisection for $x^2 = 4$ on the interval $[-3, 3]$, keeping the half whose endpoints still bracket the target. What happens?

- It finds $x = 2$.
- It finds $x = -2$.
- It cannot start: $f(-3) = f(3) = 9$, so the target is not bracketed by the endpoints' values.
- It finds both.

:::reveal
Bisection needs $f(\text{lo}) \leq y \leq f(\text{hi})$. Here both ends give 9, so nothing brackets 4 and the method has no half to keep. A non-injective function hides several answers, and a method designed for one answer must be told where to look: on $[0, 3]$ it finds 2, on $[-3, 0]$ it finds $-2$. The exercise finds all of them by scanning for sign changes first.
:::
::::

:::exercise{ref=e14}
:::

## Outside the domain

Python's `math.sqrt(-1)` raises an error. NumPy's `np.sqrt(-1.0)` returns `nan` (not a number) and keeps going, which is worse: the `nan` spreads through every later computation.

:::exercise{ref=e15}
:::

## What to take away

- Write pipelines as explicit compositions and read them in order.
- Before inverting, check the function is one-to-one on the region you care about.
- Make domain errors loud at the boundary of your code, not ten steps later as a `nan`.
