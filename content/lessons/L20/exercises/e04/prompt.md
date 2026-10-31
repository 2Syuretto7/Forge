# The fine-tuning stage: LoRA

The fine-tuning stage trains low-rank adapters on a frozen model (L16). For one linear layer:

1. `lora_forward(x, W, A, B, alpha)`: $y = x W^\top + \tfrac{\alpha}{r} x A^\top B^\top$.
2. `lora_backward(x, A, B, alpha, gy)`: the gradients of $A$ and $B$, given the gradient `gy` of the loss with respect to $y$.
3. `merge(W, A, B, alpha)`: one matrix that computes the same output, for serving without overhead.

## Hints

1. With $h = x A^\top$, the adapter output is $s\, h B^\top$ with $s = \alpha/r$, so $\partial B = s\, g_y^\top h$.
2. Backpropagate through $B$ to $h$, then through $A$: $\partial A = s\,(g_y B)^\top x$.
3. Merging adds $s\, B A$ to $W$; the served model has no adapter at all.
