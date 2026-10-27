# Recall bridge: reverse mode and hand-written backward passes

From L03: reverse mode runs a chain of vector-Jacobian products backward from a scalar, and needs the values computed in the forward pass. From L07: for an MLP you wrote every VJP by hand, layer by layer, and checked each one with finite differences. This lesson automates that work for any composition of tensor operations. Reviews due from L03 and L07 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
For $y = x_1 x_2$, the VJP with upstream gradient $g$ sends $g\,x_2$ to $x_1$ and [[g*x1]] to $x_2$.
:::
:::step
For $y = \log x$, the VJP sends $g/x$ to $x$. At $x = 4$, $g = 2$ that is [[0.5]].
:::
:::step
If $x$ feeds two operations whose VJPs send it $0.3$ and $-0.1$, its total gradient is [[0.2]].
:::
::::
