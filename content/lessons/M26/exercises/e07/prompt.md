# Softplus, sigmoid and log-sigmoid at the extremes

The binary cross-entropy of a logit $x$ needs $\log\sigma(x) = -\operatorname{softplus}(-x)$, where $\operatorname{softplus}(x) = \log(1 + e^x)$ (Section 5). Written directly, $e^x$ overflows for large $x$, and $\log(1 + e^x)$ rounds to $\log 1 = 0$ for very negative $x$.

- `softplus(x)`: stably, $\max(x, 0) + \log(1 + e^{-\lvert x\rvert})$ with `np.log1p`.
- `sigmoid(x)`: stably for both signs, from $e^{-\lvert x\rvert}$, which never overflows.
- `log_sigmoid(x)`: $-\operatorname{softplus}(-x)$.

All accept arrays. The tests run a **gradient check** (the derivative of softplus is the sigmoid, that of log-sigmoid is $1 - \sigma(x) = \sigma(-x)$), and evaluate at $x = \pm 40$ and $\pm 1000$. On a desktop they do so under a NumPy setting that turns any overflow into an error; the browser's NumPy cannot detect overflow, so there the values alone decide.

## Hints

1. With `e = np.exp(-np.abs(x))`: $\sigma(x) = 1/(1 + e)$ for $x \ge 0$ and $e/(1 + e)$ for $x < 0$.
2. `np.where` evaluates both branches, so both must be safe for every $x$.
3. $\log\sigma(40) = -\log(1 + e^{-40}) \approx -4.25 \times 10^{-18}$, not 0.
