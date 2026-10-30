# Puzzle: are these words similar?

A language model represents each word by a list of 300 numbers, an **embedding**. You cannot plot 300 dimensions, and no single coordinate means anything on its own. Yet "king" and "queen" should be close, and "king" and "carrot" should not.

::::predict{id=p1 kind=choice answer=b}
Two vectors of 300 random numbers (each drawn independently from a bell curve around 0) are compared by the cosine of the angle between them, which runs from $-1$ (opposite) through 0 (perpendicular) to 1 (same direction). What is a typical value?

- Around 0.5: random arrows are about halfway similar.
- Around $\pm 0.06$: random arrows in 300 dimensions are almost perpendicular.
- Exactly 0.
- Around $\pm 0.7$, as in two dimensions.

:::reveal
About $\pm 0.06$, which is $1/\sqrt{300}$. In two dimensions random arrows point anywhere, and the cosine is spread over the whole range. In 300 dimensions, a random arrow spreads its length over directions the other arrow barely uses, so their cosine is tiny. That is why a cosine of 0.6 between two embeddings is a strong signal: chance alone almost never produces it. M34 proves this concentration.
:::
::::

::::predict{id=p2 kind=numeric answer=36.9 tol=1.5}
Two embeddings have cosine similarity 0.8. What angle is that, in degrees?

:::reveal
$\arccos 0.8 \approx 36.9^\circ$: in the plane, the smaller angle of a 3-4-5 triangle. In 300 dimensions it is a very close pair, since random pairs sit near $90^\circ$.
:::
::::

The widget works in two dimensions, where you can see everything. You control the coordinates of two arrows $x$ and $y$; the caption computes the dot product from the coordinates and again from the lengths and the angle. Do the two always agree? When does the dot product change sign?

:::widget{name=VectorPlayground x1=2 x2=0.5 y1=1 y2=1.5}
:::

## Questions to carry into the derivation

1. What is the length of a list of 300 numbers?
2. How can a sum of products of coordinates measure an angle?
3. Why can a cosine never exceed 1, in any dimension?
4. How do you measure the part of one vector that points along another?
