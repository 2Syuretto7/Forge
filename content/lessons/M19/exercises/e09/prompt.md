# Learning a low-rank factorization by gradient descent

Eckart-Young says the truncated SVD is optimal. Here you reach the same error a different way: parametrize $X \approx UV^\top$ with $U \in \mathbb{R}^{m \times k}$, $V \in \mathbb{R}^{n \times k}$ and minimize

$$
L(U, V) = \tfrac{1}{2}\, \|X - U V^\top\|_F^2 .
$$

With residual $R = X - UV^\top$, the gradients are $\nabla_U L = -RV$ and $\nabla_V L = -R^\top U$. Derive them yourself by perturbing $U \to U + \epsilon E$ and keeping the first-order term, then implement:

- `loss(U, V, X)` returns a float.
- `grads(U, V, X)` returns `(dU, dV)` with the shapes of `U` and `V`.
- `fit(X, k, steps, lr, seed)`: initialize `U` and `V` with `0.1 * rng.normal(size=...)` from `np.random.default_rng(seed)` (first `U`, then `V`), run plain gradient descent, and return `(U, V)`.

The test checks that your fitted product reaches the Eckart-Young error within one percent. This low-rank structure (M14) is exactly what LoRA trains in L16; the gradients are two matmul VJPs.

## Hints

1. `R = X - U @ V.T`; `loss = 0.5 * np.sum(R ** 2)`.
2. `dU = -R @ V`, `dV = -R.T @ U`.
3. Update both from the same residual: compute both gradients, then step.
