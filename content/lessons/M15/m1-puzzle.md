# Puzzle: zoom until it looks straight

Plot $f(x) = x^2$ near $x = 1$ and zoom in. At each halving of the window the curve looks a little straighter; after a dozen halvings it is indistinguishable from a line.

::::predict{id=p1 kind=numeric answer=2 tol=0.01}
What is the slope of the line that $x^2$ turns into near $x = 1$?

:::reveal
2. The secant from $1$ to $1 + h$ has slope $\frac{(1 + h)^2 - 1}{h} = 2 + h$, and as the window shrinks, $h \to 0$ and the slope approaches 2. That limit is the **derivative**, $f'(1) = 2$. Zooming is the picture; the limit is the definition.
:::
::::

::::predict{id=p2 kind=choice answer=c}
Now zoom in on the ReLU, $\max(0, x)$, at $x = 0$. What do you see after twenty halvings?

- A straight line of slope $1/2$.
- A horizontal line.
- The same corner as before: a flat piece meeting a piece of slope 1, however far you zoom.
- A smooth curve.

:::reveal
The same corner. The ReLU looks identical at every scale near 0: the slope from the left is 0 and from the right is 1, at every zoom level. No single line approximates it, so it has no derivative at 0. Neural networks are full of such corners; Section 6 says what frameworks do about them.
:::
::::

Try both, and the cube root at 0, which zooms into a vertical line.

:::widget{name=TangentZoom f=square a=1 zoom=0}
:::

## Questions to carry into the derivation

1. What does "approaches" mean, precisely, when the input varies continuously?
2. Why should zooming in make a curve look straight, and what is the slope?
3. Can the rules for derivatives be proved, rather than memorized?
4. If the derivative is a limit as $h \to 0$, why not compute it with $h = 10^{-15}$?
