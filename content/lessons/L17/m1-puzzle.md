# Puzzle: an update that disappears

A weight equals 1.0. Each training step adds 0.001 to it. After 1000 steps it should be 2.0.

::::predict{id=p1 kind=choice answer=a}
The weight is stored in bf16 (7 mantissa bits) and each update is rounded to the nearest bf16 value. What is it after 1000 steps?

- Still 1.0.
- About 2.0.
- About 1.5.
- Infinity.

:::reveal
Near 1.0, consecutive bf16 numbers are $2^{-7} \approx 0.0078$ apart. Adding 0.001 gives $1.001$, whose nearest bf16 neighbour is 1.0: the update rounds away, every time. This is why mixed-precision training keeps a full-precision master copy of the weights, or uses stochastic rounding.
:::
::::

::::predict{id=p2 kind=numeric answer=65504 tol=1}
What is the largest finite fp16 number?

:::reveal
$(2 - 2^{-10}) \cdot 2^{15} = 65504$. Activations, attention scores or a loss multiplied by a scale factor can exceed it and become infinite. bf16 reaches about $3.4 \times 10^{38}$, like fp32, because it keeps fp32's 8 exponent bits.
:::
::::

Explore the formats in the widget: choose a value, and compare how each format stores it.

:::widget{name=FloatFormats value=0.1}
:::
