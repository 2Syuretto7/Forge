# Break it: attention without the square root

Drop the $1/\sqrt d$ from attention and the scores have standard deviation $\sqrt d$ (e03). For $d = 1024$ that is 32: the softmax puts nearly all its weight on one key, and its Jacobian, $\mathrm{diag}(p) - pp^\top$, nearly vanishes, so almost no gradient flows back into the scores (Section 3).

- `softmax(z)`: stable, for a vector.
- `softmax_jacobian(z)`: $\mathrm{diag}(p) - pp^\top$.
- `attention_stats(d, n_keys, scaled, trials, rng)`: for `trials` random queries against `n_keys` random keys (standard normal entries), the mean of the largest attention weight and the median Frobenius norm of the softmax Jacobian, as a tuple.

The tests run a **gradient check** of the Jacobian, then find the unscaled softmax saturated at $d = 1024$ (largest weight above 0.9, Jacobian norm below a tenth of its scaled value) while the scaled one behaves the same at every width.

## Hints

1. Subtract the maximum before exponentiating.
2. The Jacobian's entries are $p_i(\delta_{ij} - p_j)$.
3. A few near-ties between the top two scores keep the mean Jacobian norm up; the median shows the typical query. Saturation is not an error: nothing crashes, the loss simply stops improving.
