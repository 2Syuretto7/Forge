# Categorical MLE through a softmax

A categorical distribution over $K$ outcomes can be parametrized by unconstrained **logits** $z \in \mathbb{R}^K$ through the softmax, $\pi_j = e^{z_j} / \sum_k e^{z_k}$. Given outcome counts $c \in \mathbb{N}^K$ with total $N$, the negative log-likelihood is

$$
J(z) = -\sum_j c_j \log \pi_j(z).
$$

- `softmax(z)`: numerically stable (subtract `max(z)` first).
- `nll(z, counts)`: compute $\log \pi$ stably as $z - \operatorname{logsumexp}(z)$.
- `grad_nll(z, counts)`: derive it; you should find $N\pi - c$.
- `mle_probs(counts)`: the closed-form MLE, $c / N$.

This is the same gradient that drives every classifier and language model in the course (L05, L07, L14).

## Hints

1. `logsumexp(z) = m + log(sum(exp(z - m)))` with `m = max(z)`.
2. $\partial \log \pi_j / \partial z_i = \mathbb{1}[i = j] - \pi_i$.
3. At $z = \log(c/N)$ the gradient is zero.
