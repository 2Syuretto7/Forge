# A LoRA layer

LoRA keeps a pretrained weight $W_0$ ($d_\text{out} \times d_\text{in}$) frozen and learns a low-rank update: $A$ ($r \times d_\text{in}$) and $B$ ($d_\text{out} \times r$), scaled by $\alpha/r$:
$$
y = x W_0^\top + \frac{\alpha}{r}\,(x A^\top) B^\top.
$$

1. `lora_forward(x, W0, A, B, alpha)`.
2. `lora_backward(dy, x, W0, A, B, alpha)`: the gradients with respect to $A$, $B$ and $x$.

## Hints

1. With $h = x A^\top$ and $s = \alpha/r$: $\partial B = s\, dy^\top h$ and $\partial A = s\,(dy\, B)^\top x$.
2. $\partial x$ has a frozen path and an adapter path: $dy\, W_0 + s\,(dy\, B) A$.
3. LoRA starts with $B = 0$, so the adapted model begins exactly at the pretrained one.
