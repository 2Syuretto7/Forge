# Exponential families have convex negative log-likelihoods

A categorical distribution with natural parameters $\theta \in \mathbb{R}^K$ has $p_k = e^{\theta_k - A(\theta)}$ with the **log-partition** $A(\theta) = \log\sum_k e^{\theta_k}$. Its gradient is the mean of the one-hot outcome, $\nabla A = p$, and its Hessian is the covariance, $\operatorname{diag}(p) - pp^\top \succeq 0$: $A$ is convex. The negative log-likelihood of counts $c$ is $N A(\theta) - c^\top\theta$, a convex function plus a linear one (Section 5).

- `log_partition(theta)` and `grad_log_partition(theta)`.
- `nll(theta, counts)`.
- `fit(counts, steps=500, lr=1.0)`: gradient descent on the average negative log-likelihood from $\theta = 0$, returning $\theta$; because the problem is convex, it reaches the global minimum, where $p = c/N$.

The tests run a **gradient check** of `grad_log_partition`, confirm the Hessian is a covariance matrix, and fit.

## Hints

1. Stable log-sum-exp from M26.
2. The gradient of the average NLL is $p - c/N$.
3. $\theta$ is determined only up to adding a constant to every entry; compare probabilities, not parameters.
