# Training an adapter

Fit a LoRA adapter to a known target update by gradient descent, and compare with the best possible rank-$r$ error.

Implement `fit_lora(target, r, alpha, steps=3000, lr=0.05, seed=0)`: minimize $\tfrac12 \|\frac{\alpha}{r} B A - \Delta\|_F^2$, starting as LoRA does from $B = 0$ and $A$ with entries $\mathcal{N}(0, 1/r)$ (drawn with `np.random.default_rng(seed)`). Return $A$, $B$ and the final loss.

## Hints

1. With $E = \frac{\alpha}{r} B A - \Delta$: $\partial B = \frac{\alpha}{r} E A^\top$, $\partial A = \frac{\alpha}{r} B^\top E$.
2. Update $A$ and $B$ from gradients computed at the same point.
3. Gradient descent on this factorization reaches the SVD optimum: its only minima are global.
