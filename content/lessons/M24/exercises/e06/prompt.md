# Moment generating functions

The moment generating function $M(t) = \mathbb{E}e^{tX}$ packs every moment into one function: $M'(0) = \mathbb{E}X$, $M''(0) = \mathbb{E}X^2$, and the MGF of a sum of $n$ independent copies is $M(t)^n$ (Section 3).

- `mgf_bernoulli(t, p)` $= 1 - p + pe^t$, `mgf_normal(t, mu, sigma)` $= e^{\mu t + \sigma^2 t^2/2}$, and `mgf_exponential(t, lam)` $= \lambda/(\lambda - t)$ for $t < \lambda$.
- `moments_from_mgf(M, h=1e-4)`: the first and second moments from central differences at 0, $\frac{M(h) - M(-h)}{2h}$ and $\frac{M(h) - 2M(0) + M(-h)}{h^2}$.
- `mgf_of_sum(M, n)`: the function $t \mapsto M(t)^n$.

The tests run a **gradient check** of the moments read off each MGF against the known means and second moments, confirm that the sum's MGF matches the binomial's, and watch the log-MGF of a standardized sum approach $t^2/2$, the normal's: the idea behind the proof of the central limit theorem.

## Hints

1. Use `np.exp` so that the MGFs accept arrays.
2. `mgf_of_sum` returns a function: `lambda t: M(t) ** n`.
3. The exponential's second moment is $2/\lambda^2$.
