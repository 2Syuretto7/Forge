# Speculative decoding

A small draft model proposes tokens; the large target model checks several of them in one forward pass. The acceptance rule keeps the output distribution **exactly** the target's.

1. `emitted_distribution(p, q)`: draw $x \sim q$, accept with probability $\min(1, p(x)/q(x))$, else draw from $\max(0, p - q)$ renormalized. Return the exact distribution of the emitted token: it must equal $p$.
2. `acceptance_rate(p, q)`: $\sum_x \min(p(x), q(x))$.
3. `acceptance_grad(p, z)`: the gradient of the acceptance rate with respect to the draft's logits $z$ ($q = \operatorname{softmax}(z)$), the quantity a draft model can be trained to raise.
4. `expected_tokens(alpha, gamma)`: tokens per target call with $\gamma$ drafted tokens each accepted with probability $\alpha$: $(1 - \alpha^{\gamma + 1})/(1 - \alpha)$.

## Hints

1. Accepted mass at $x$: $q(x)\min(1, p/q) = \min(p, q)$. Rejected mass $1 - \sum \min(p, q)$ is spread as the residual, which is exactly $p - \min(p, q)$.
2. $\partial \min(p, q)/\partial q = 1$ where $q < p$, else 0; then chain through the softmax.
3. A draft distilled from the target (L20) raises $\alpha$.
