# Break it: cross-entropy from probabilities

A classifier produces logits $z$; the loss for the correct class $y$ is $-\log\operatorname{softmax}(z)_y$. Computing the probabilities first and then their logarithm fails as soon as a probability underflows to 0, and in float32 that happens at a logit gap of about 104.

- `ce_from_probs(z, y)`: `-np.log(p[y])` with `p` a softmax computed by `np.exp(z) / np.sum(np.exp(z))` after subtracting the maximum, in the dtype of `z`.
- `ce_from_logits(z, y)`: $\operatorname{logsumexp}(z) - z_y$, stably, in the dtype of `z`.
- `first_failure(dtype)`: the smallest integer gap $g$ for which `ce_from_probs(np.array([g, 0], dtype), 1)` is infinite.

The tests find the failure point in float32 and float64, and confirm that the logits version returns the exact loss, the gap itself, far beyond it.

## Hints

1. Subtracting the max avoids overflow but not underflow: $e^{-g}$ still rounds to 0.
2. Silence the expected warning with `np.errstate(divide="ignore")` in `ce_from_probs`.
3. Search upward from 1; the answers are near 104 for float32 and 746 for float64.
