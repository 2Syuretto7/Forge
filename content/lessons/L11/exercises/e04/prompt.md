# Hoffmann's fitting objective

Hoffmann et al. fit $L(N, D) = E + A N^{-\alpha} + B D^{-\beta}$ by minimizing, over all runs, the Huber loss of the error in $\log L$. Writing $A = e^a$, $B = e^b$, $E = e^e$, the predicted log loss is a log-sum-exp:
$$
\log \hat L = \operatorname{LSE}(a - \alpha \log N,\; b - \beta \log D,\; e).
$$

1. `huber(r, delta)`: elementwise $\tfrac12 r^2$ for $|r| \le \delta$ and $\delta(|r| - \tfrac12\delta)$ beyond, and its derivative.
2. `hoffmann_objective(theta, N, D, L, delta=1e-3)` with $\theta = (a, b, e, \alpha, \beta)$: return $\sum_i \operatorname{huber}(\log \hat L_i - \log L_i, \delta)$ and its gradient with respect to $\theta$.

## Hints

1. The derivative of LSE with respect to each argument is the softmax weight of that argument.
2. Subtract the largest of the three terms before exponentiating.
3. The gradient with respect to $\alpha$ is $-\sum_i h'(r_i)\, p_{i,1} \log N_i$, where $p_{i,1}$ is the weight of the first term.
