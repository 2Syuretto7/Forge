# Break it: wrong order, wrong transpose, silent broadcasting

## Multiply in the wrong order

Rotate a shape about its centre and then move it, or move it and then rotate about the origin: the pictures differ, and code that composes matrices in the wrong order draws the second while you meant the first.

:::exercise{ref=e13}
:::

## Transpose the wrong factor

A linear layer stores its weights as $W$ of shape (outputs, inputs) and computes $y = x W^\top + b$ for a batch $x$ of shape (batch, inputs). Forget the transpose and the code fails loudly, unless the layer is square.

:::exercise{ref=e14}
:::

## Broadcast across the wrong axis

::::predict{id=p5 kind=choice answer=d}
`x` has shape `(100,)` and `w` has shape `(100, 1)`. What does `x - w` produce?

- An error: the shapes differ.
- Shape `(100,)`: the extra axis is dropped.
- Shape `(100, 1)`.
- Shape `(100, 100)`: every entry of `x` minus every entry of `w`.

:::reveal
Shape `(100, 100)`, without a warning. NumPy lines the shapes up from the right, `(100,)` becomes `(1, 100)`, and each axis of size 1 stretches to match the other. A loss computed from that array is a wrong number of the right type, the most expensive kind of bug.
:::
::::

:::exercise{ref=e15}
:::

:::widget{name=MatrixTransform a=1 b=2 c=0.5 d=1}
:::

This matrix has determinant 0: the ellipse has collapsed to a segment and the grid to a line. Every point of that line came from a whole line of inputs, so nothing can undo the map.

## What to take away

- $AB$ applies $B$ first. Write pipelines as a list in the order applied and multiply from the right.
- Check shapes when a square matrix could hide a missing transpose.
- Assert shapes before subtracting arrays that should match exactly.
