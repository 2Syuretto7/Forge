# Recall bridge: eigenvalues and the training loop

Two earlier lessons carry this one. From M13 and M28: a symmetric matrix $A = Q \Lambda Q^\top$ has orthogonal eigenvectors, and the ratio of its largest to smallest eigenvalue is its **condition number** $\kappa$. From L03: training repeats forward, backward and the update $\theta \leftarrow \theta - \eta \nabla L$ on minibatches. Near a minimum every smooth loss looks like a quadratic whose Hessian has some condition number, and this lesson shows that $\kappa$ decides how fast that update can go. Reviews due from M13, L03 and L04 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
For $f(x) = \tfrac12 a x^2 - b x$, the derivative is $f'(x) =$ [[a*x - b]].
:::
:::step
The Hessian of $f(x, y) = \tfrac12 (x^2 + 100 y^2)$ is $\operatorname{diag}(1, 100)$. Its condition number is [[100]].
:::
:::step
An SGD step with learning rate $0.1$ on a weight whose gradient is $0.5$ changes it by [[-0.05]].
:::
::::

By the end of this lesson you will have built gradient descent, heavy-ball momentum, Adam and AdamW, warmup and cosine schedules, and Xavier and He initialization from scratch, and raced them on the L03 digit task.
