# Maximum likelihood equals minimum cross-entropy

Fit a categorical model $q = \operatorname{softmax}(z)$ to observed data and confirm Section 4 numerically. `data` is a 1-D integer array of observed classes in $\{0, \dots, K-1\}$.

- `empirical(data, K)`: the empirical distribution $\hat p$.
- `avg_nll(z, data)`: $-\frac{1}{n}\sum_i \log q_{x_i}$ computed stably.
- `grad_avg_nll(z, data, K)`: its gradient with respect to $z$. Derive it: you should get $q - \hat p$.
- `fit(data, K, steps, lr)`: gradient descent from $z = 0$. Return $\operatorname{softmax}(z)$.

The tests verify that `avg_nll` equals the cross-entropy $H(\hat p, q)$, that your gradient passes a finite-difference check, and that the fit converges to $\hat p$.

## Hints

1. `np.bincount(data, minlength=K) / len(data)`.
2. $\log q_j = z_j - \operatorname{LSE}(z)$.
3. Gradient descent with `lr=1` converges quickly here because the problem is convex in $z$.
