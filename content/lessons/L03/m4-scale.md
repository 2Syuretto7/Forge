# Scale and measure: costs, curvature and memory

This movement measures the claims of Sections 4 and 7: that the two modes of differentiation cost a pass per input or per output, that reverse mode trades computation for memory, and that the size of a safe gradient step is set by curvature.

## Counting passes

:::exercise{ref=e10}
:::

::::predict{id=p4 kind=choice answer=b}
A network has $10^8$ parameters and one scalar loss. Computing the full gradient with reverse mode costs roughly how much compared with evaluating the loss once?

- About $10^8$ times as much.
- A small constant factor, typically two to four times.
- Exactly the same.
- It depends on the number of layers squared.

:::reveal
One reverse pass computes a VJP for every operation in the forward pass, and each VJP costs about as much as the operation itself (matrix multiplies cost twice: one product for the input gradient and one for the weight gradient). So the backward pass costs about two forward passes, and the whole gradient about three. This is why training is only a few times more expensive than inference per example.
:::
::::

## Memory: what reverse mode must remember

:::exercise{ref=e13}
:::

Your reverse pass stored one value per function in the chain. In a network, the stored values are the activations of every layer for every example in the batch. For a transformer with 24 layers, a batch of 32 sequences of 2,048 tokens and a width of 2,048, a single activation tensor per layer already holds $24 \times 32 \times 2048 \times 2048 \approx 3.2 \times 10^9$ numbers. L18 shows how to trade some of that memory back for recomputation.

## Curvature and the step size

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::

The curvature bound $L$ you just measured sets the largest stable learning rate. L09 derives convergence rates from it, by way of L07's networks.
