# Scale: twenty layers and a growing number of inputs

Differentiate a 20-layer composition, $f = f_{20} \circ \dots \circ f_1$ from $\mathbb{R}^n$ to $\mathbb{R}$, both ways, and time it as $n$ grows. Forward mode's cost grows with $n$; reverse mode's stays flat.

::::predict{id=p4 kind=choice answer=a}
$f: \mathbb{R}^{10} \to \mathbb{R}^{10000}$, and you need its full Jacobian. Which mode is cheaper?

- Forward: 10 passes against 10,000.
- Reverse: it always is.
- Either: the Jacobian has the same entries.
- Neither works for such shapes.

:::reveal
Forward mode, with 10 JVP passes, one per input. Reverse mode needs one VJP pass per output, 10,000. Neural network training has the opposite shape, millions of inputs and one loss, which is why frameworks are built around reverse mode; sensitivity analyses with few parameters and many outputs use forward mode.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
