# Scores of a mixture

The **score** of a density is $\nabla_x\log p(x)$: the direction in which the density increases fastest, relative to its size (Section 4). It does not need the normalizing constant, and for a Gaussian mixture it has a clean form: a responsibility-weighted average of the components' scores,

$$
\nabla\log p(x) = \sum_kr_k(x)\,\frac{m_k - x}{s_k^2}, \qquad r_k(x) = \frac{w_k\,N(x; m_k, s_k^2)}{p(x)} .
$$

- `mixture_logpdf(x, w, m, s)`: for an array `x` of points in one dimension, using log-sum-exp (M26).
- `mixture_score(x, w, m, s)`.
- `responsibilities(x, w, m, s)`: an array of shape `(len(x), K)`.

The tests run a **gradient check** of the score against finite differences of the log density, including far in the tails where a naive computation underflows.

## Hints

1. Compute the log of each weighted component density, subtract the row maximum, exponentiate and normalize to get the responsibilities.
2. Far from every component, $p(x)$ underflows to 0 in floating point, but the responsibilities and the score stay finite if computed in log space.
3. Near a component the score points to its mean; between components it points toward the more likely one.
