# Log-sum-exp and log-softmax

- `logsumexp(z)`: $\ln \sum_j e^{z_j}$, computed as $c + \ln \sum_j e^{z_j - c}$ with $c = \max z$.
- `log_softmax(z)`: the list $z_i - \operatorname{LSE}(z)$, the logarithms of the softmax probabilities, computed without ever forming a probability.
- `nll(z, target)`: the negative log-likelihood of class `target`: minus its log-softmax. This is the cross-entropy loss of one example, which every classifier and language model minimizes.

The tests check against direct formulas on small scores, on huge scores where direct formulas overflow, and the bounds $\max z \leq \operatorname{LSE}(z) \leq \max z + \ln n$.

## Hints

1. `m = max(z); return m + math.log(sum(math.exp(v - m) for v in z))`.
2. Compute `logsumexp` once and subtract it from each score.
3. `-log_softmax(z)[target]`.
