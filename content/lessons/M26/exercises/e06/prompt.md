# Log-sum-exp and softmax that never overflow

$\log\sum_i e^{z_i}$ overflows for $z_i$ around 710 in float64 (89 in float32) and underflows to $\log 0$ for very negative $z_i$. Subtracting the maximum $m$ fixes both (Section 5):

$$
\log\sum_i e^{z_i} = m + \log\sum_i e^{z_i - m} .
$$

- `naive_logsumexp(z)`: the formula as written.
- `logsumexp(z)`: the stable version, for a 1-D array.
- `softmax(z)`: $e^{z - \operatorname{logsumexp}(z)}$.

The tests run a **gradient check**: the gradient of log-sum-exp is the softmax.

## Hints

1. Every $z_i - m \le 0$, so no exponential exceeds 1, and the largest equals 1, so the sum is at least 1.
2. Computing softmax through log-sum-exp keeps it accurate when one probability is nearly 1.
3. Use `np.errstate(over="ignore")` only in the naive version, to let it overflow quietly.
