# Break it: naive softmax cross-entropy

Watch the textbook formula fail, then fix it.

- `naive_softmax(z)`: exactly $e^{z}/\sum e^{z}$, with no stabilization.
- `naive_logprob(z, y)`: `np.log(naive_softmax(z)[y])`.
- `stable_logprob(z, y)`: $z_y - \operatorname{LSE}(z)$ with the max-subtraction trick.

Run these in the dtype of the input. The tests show two different failures of the naive version: overflow in float64 for large logits (`inf / inf` gives `nan`), and underflow in float32 for a strongly disfavored class (the probability rounds to 0 and its log is `-inf`). The stable version handles both.

## Hints

1. Write the naive versions plainly; they are supposed to break.
2. `m = z.max(); z[y] - (m + np.log(np.sum(np.exp(z - m))))`.
3. Keep the input dtype: do not convert float32 inputs to float64.
