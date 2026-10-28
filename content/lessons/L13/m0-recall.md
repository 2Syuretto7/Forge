# Recall bridge: dot products, softmax, backprop and residual blocks

Five earlier lessons meet here. From L01, a dot product measures how much two vectors point the same way. From L05, the softmax turns scores into probabilities, with Jacobian $\operatorname{diag}(p) - pp^\top$. From L07, a matrix product $Y = XW$ sends gradients $G W^\top$ and $X^\top G$. From L10, a pre-norm residual block computes $x + F(\operatorname{LN}(x))$. From L11, an operation's speed is set by its arithmetic intensity. Reviews due from those lessons appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
The dot product of $(1, 2, 0)$ and $(3, -1, 4)$ is [[1]].
:::
:::step
The softmax of the scores $(0, \ln 3)$ puts weight [[0.75]] on the second entry.
:::
:::step
For $Y = XW$ with $X$ of shape $10 \times 4$ and $W$ of shape $4 \times 4$, the gradient with respect to $W$, $X^\top G$, has [[16]] entries.
:::
::::
