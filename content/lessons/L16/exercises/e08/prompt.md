# Mixing domains

A pretraining set mixes domains (web, books, code, papers) of very different sizes. Sampling weights decide how many tokens each contributes and how often its data repeats.

1. `domain_epochs(weights, sizes, total_tokens)`: the number of passes over each domain.
2. `temperature_weights(sizes, tau)`: weights proportional to $\text{size}^{1/\tau}$; $\tau = 1$ samples by size and larger $\tau$ moves toward uniform, upsampling small domains.
3. `mixture_objective(z, c, beta, T)`: with $p = \operatorname{softmax}(z)$, domain $j$'s excess loss after $p_j T$ tokens is $c_j (p_j T)^{-\beta}$. Return the total and its gradient with respect to $z$.
4. `optimal_mixture(c, beta)`: the weights minimizing $\sum_j c_j p_j^{-\beta}$ subject to $\sum_j p_j = 1$.

## Hints

1. The gradient with respect to $p_j$ is $-\beta L_j / p_j$; through the softmax, $\partial/\partial z = p \odot (g - p^\top g)$.
2. A Lagrange multiplier gives $\beta c_j p_j^{-\beta - 1} = \lambda$, so $p_j \propto c_j^{1/(1+\beta)}$.
3. Domains with more to learn get more weight, but less than proportionally.
