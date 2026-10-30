# Scale: a thousand points and a thousand pieces

The derivation predicted that the error of straight pieces falls like $1/n^2$. Now measure it: fit the hill with 10, 100 and 1,000 pieces, at a thousand test points, with NumPy doing the work.

::::predict{id=p4 kind=choice answer=c}
You measure the largest error of the piecewise-linear hill with 10, 20, 40, 80 and 160 pieces. By what factor does the error shrink at each doubling?

- About 2.
- About 3.
- About 4.
- About 8.

:::reveal
About 4, the $h^2$ law: halving the piece length quarters the gap between a smooth curve and its chords. On a log-log plot of error against the number of pieces, the points fall on a line of slope $-2$; the exercise fits that slope.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

## Curves that bend without limit

Try the widget with the sine curve and then with the cubic. Each smooth curve settles into the same factor of four. The last exercise of this movement finds a curve that does not.

:::widget{name=FunctionMachine mode=relu target=sine n=8}
:::

:::exercise{ref=e12}
:::
