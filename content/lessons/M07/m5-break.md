# Break it: wrong units and shrinking shapes

Two failures are typical of trigonometric code. Mixing degrees and radians gives plausible numbers that are wrong. A rotation that is slightly off (its cosine and sine rounded, say) is not a rotation at all: it scales the plane a tiny bit at every step, and after thousands of steps the shape has visibly grown or shrunk.

## Degrees in a radian function

:::exercise{ref=e13}
:::

## A rotation that is not quite a rotation

::::predict{id=p5 kind=choice answer=c}
You build a rotation matrix from $\cos\theta$ and $\sin\theta$ each rounded to 3 decimal places, and apply it 10,000 times. What happens to the distance of a point from the origin?

- Nothing: rounding the entries cannot change lengths.
- It drifts randomly up and down.
- It changes by a fixed factor every step, very close to 1, so after 10,000 steps it has grown or shrunk by a visible amount.

:::reveal
The matrix with entries $c, -s, s, c$ multiplies every length by exactly $\sqrt{c^2 + s^2}$. With entries rounded for $\theta = 37^\circ$ that factor is not 1 but $1.0004$, and 10,000 steps raise it to the 10,000th power: about $e^{4} \approx 56$. Small per-step errors compound geometrically, just like interest. Renormalizing the matrix (dividing $c$ and $s$ by $\sqrt{c^2 + s^2}$) restores exact length preservation.
:::
::::

The circle in the widget is exact; your matrix is not. Rotate by an angle whose cosine and sine you round in your head, and see whether the arrow stays on the circle.

:::widget{name=UnitCircle theta=37 phi=-37 r=1}
:::

:::exercise{ref=e14}
:::

:::exercise{ref=e15}
:::

## What to take away

- Radians in, radians out. Convert at the boundary of your code, once.
- A rotation must preserve length exactly; check $c^2 + s^2 = 1$ and renormalize after rounding.
- Errors that multiply compound like interest: a per-step factor of $1 + \varepsilon$ becomes $e^{k\varepsilon}$ after $k$ steps.
