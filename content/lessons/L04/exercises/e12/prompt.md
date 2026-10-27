# Binary cross-entropy from logits

For a binary label $y \in \{0, 1\}$ and a logit $a$ (so $P(y=1) = \sigma(a)$), the loss $-y\log\sigma(a) - (1-y)\log(1-\sigma(a))$ simplifies to the stable form

$$
\ell(a, y) = \max(a, 0) - a\,y + \log\big(1 + e^{-|a|}\big).
$$

- `bce_with_logits(a, y)`: elementwise stable loss for arrays `a`, `y`.
- `bce_grad(a, y)`: derive it; you should find $\sigma(a) - y$.
- `binary_entropy(p)`: in nats, with $0\log 0 = 0$.

The minimum over $a$ of the expected loss when $y \sim \text{Bernoulli}(p)$ is the binary entropy $h(p)$; one test checks this.

## Hints

1. Verify the stable form by checking the cases $a \ge 0$ and $a < 0$ separately.
2. `np.log1p(np.exp(-np.abs(a)))` is accurate for large $|a|$.
3. The best logit for $y \sim \text{Bernoulli}(p)$ is $\log\frac{p}{1-p}$.
