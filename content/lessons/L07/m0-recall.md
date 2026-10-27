# Recall bridge: VJPs and softmax regression

Two earlier lessons carry this one. From L03: reverse mode composes vector-Jacobian products, and a matrix product $Y = XW$ has VJPs $GW^\top$ and $X^\top G$. From L05: softmax regression has gradient $\tfrac1n X^\top(P - Y)$ with respect to its weights. A neural network is softmax regression on top of features that are themselves computed by layers like it, and its gradient is those two facts applied layer by layer. Reviews due from L03 and L05 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
For $Y = XW$ with $X$ of shape $32 \times 10$ and $W$ of shape $10 \times 4$, the gradient $\partial L/\partial W = X^\top G$ has shape $10 \times 4$. The number of entries is [[40]].
:::
:::step
The softmax cross-entropy gradient with respect to the logits of one example is $p - e_y$. If $p = (0.1, 0.7, 0.2)$ and $y$ is the first class, the first entry of the gradient is [[-0.9]].
:::
:::step
The derivative of $\tanh$ at a point where $\tanh(z) = 0.6$ is $1 - 0.6^2 =$ [[0.64]].
:::
::::
