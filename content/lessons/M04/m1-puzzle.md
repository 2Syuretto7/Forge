# Puzzle: drawing a hill with ramps

The function $\operatorname{relu}(x) = \max(0, x)$ is zero for negative inputs and the identity for positive ones: a flat floor, then a ramp. It is the most common building block in neural networks, and it is about as simple as a function can be.

Now combine shifted copies. $\operatorname{relu}(x) - \operatorname{relu}(x - 1)$ rises from 0 to 1 between $x = 0$ and $x = 1$ and then stays flat. Subtract a second, shifted ramp and you get a triangle, a bump. Bumps can be stacked. So with enough ReLU pieces you can draw any curve, roughly.

::::predict{id=p1 kind=choice answer=b}
The smooth hill $e^{-x^2}$ on the interval from $-3$ to $3$ is to be drawn by straight pieces (equivalently, a sum of shifted ReLUs) whose corners lie on the hill, equally spaced. How many pieces do you need so that the drawing is never more than 0.01 away from the hill?

- About 3.
- About 30.
- About 300.
- About 3,000.

:::reveal
About 30: 29 pieces miss by 0.0106 somewhere, 30 pieces by at most 0.0097. That is fewer than many people guess, because a straight piece hugs a smooth curve very closely: halve the piece length and the error falls by a factor of four. You will derive that factor of four, and in Movement 5 meet a curve for which it fails.
:::
::::

Try it in the widget: switch to drawing with ReLUs, pick the hill, and slide the number of pieces.

:::widget{name=FunctionMachine mode=relu target=bump n=6}
:::

## Machines in a row

Back in the widget's first mode, a function is a machine with one input slot and one output. Joining two machines, the output of one becoming the input of the next, is **composition**, and it is how every neural network, every data pipeline and every formula is built.

::::predict{id=p2 kind=numeric answer=-6 tol=0.01}
Let $f$ square its input and $g$ add 1 to it. What is $g(f(3)) - f(g(3))$?

:::reveal
$g(f(3)) = 3^2 + 1 = 10$ and $f(g(3)) = (3 + 1)^2 = 16$, so the difference is $-6$. The same two machines in the other order give a different machine. In general $(x + 1)^2 - (x^2 + 1) = 2x$, which is zero only at $x = 0$.
:::
::::

## Questions to carry into the derivation

1. What exactly is a function, and what are its domain and codomain?
2. When can a machine be run backwards?
3. How do shifting, stretching and reflecting a graph come from composition?
4. Why does the error of straight pieces fall like the square of their length?
