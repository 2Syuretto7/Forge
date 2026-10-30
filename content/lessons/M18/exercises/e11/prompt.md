# Checking a huge gradient in a few evaluations

Instead of $n$ partial derivatives, compare the gradient with the slope along a few random directions $u$: $\nabla f \cdot u$ against $(f(x + hu) - f(x - hu))/(2h)$.

- `directional_check(f, grad, x, k=5, h=1e-4, seed=0)`: for `k` random unit directions, the largest relative difference $|a - b| / \max(|a|, |b|, 10^{-12})$; $2k$ evaluations in all.
- `buggy_grad(grad, i)`: a function returning `grad(x)` with entry `i` doubled, a single-coordinate bug.

The step is larger than usual because $f$ is a sum of 10,000 terms: its value is in the thousands, so the rounding error of $f(x \pm hu)$, about $\varepsilon|f|$, divided by $h = 10^{-6}$ would already be $10^{-6}$. With $h = 10^{-4}$ a correct gradient gives about $10^{-8}$; a single wrong entry among 10,000 still shifts the directional slope by far more than that, so a handful of random directions catches it.

## Hints

1. `u = rng.normal(size=n); u /= np.linalg.norm(u)`.
2. Keep the worst of the `k` relative differences.
3. Copy the gradient before changing an entry.
