# LoRA, step 3: training the factors

Train LoRA on a linear model: inputs $X$, targets $Y = X(W_0 + \Delta W) + \text{noise}$, loss $\frac1{2n}\lVert X(W_0 + BA) - Y\rVert^2$. With $G = X^\top(XW - Y)/n$, the gradient of the loss with respect to $W$, the chain rule gives (Section 3)

$$
\nabla_B = GA^\top, \qquad \nabla_A = B^\top G .
$$

LoRA initializes $B = 0$ and $A$ small and random, so training starts exactly at $W_0$.

- `loss(B, A, X, Y, W0)` and `grads(B, A, X, Y, W0)`: the loss and `(grad_B, grad_A)`.
- `train_lora(X, Y, W0, r, steps=1500, lr=0.1, seed=0)`: gradient descent from $B = 0$, $A \sim N(0, 0.01)$; return `(B, A)`.

The tests run a **gradient check** of both gradients, and train rank 4 on a task whose true update has rank 4, reaching a loss within 5 percent of full least-squares fine-tuning.

## Hints

1. Write $W = W_0 + BA$ once, compute the residual $XW - Y$, then $G$.
2. With $B = 0$, the gradient of $A$ is zero at the first step: only $B$ moves first. For training, compute $X^\top X/n$ and $X^\top Y/n$ once: then $G = (X^\top X/n)W - X^\top Y/n$ costs nothing that grows with $n$.
3. The full fine-tuning optimum is the least-squares solution `np.linalg.lstsq(X, Y)`. A learning rate of 0.1 is stable here; 0.3 diverges, because the factors' scales multiply.
