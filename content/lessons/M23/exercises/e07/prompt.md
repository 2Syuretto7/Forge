# Fusing measurements: precisions add

Two independent Gaussian measurements of the same quantity, $N(m_1, v_1)$ and $N(m_2, v_2)$, combine by multiplying their densities (Section 6). The product is Gaussian with

$$
\frac{1}{v} = \frac{1}{v_1} + \frac{1}{v_2}, \qquad m = v\left(\frac{m_1}{v_1} + \frac{m_2}{v_2}\right) .
$$

Precisions (inverse variances) add, and the mean is the precision-weighted average.

- `fuse(m1, v1, m2, v2)`: the combined `(m, v)`.
- `fuse_many(means, variances)`: fuse a whole list.
- `gain(prior_var, meas_var)`: the Kalman gain $K = v_1/(v_1 + v_2)$, so that the fused mean is $m_1 + K(m_2 - m_1)$.

## Hints

1. Work with precisions $1/v$ and sum them.
2. `fuse_many` of $n$ equal variances $v$ gives $v/n$: the average of $n$ measurements.
3. The fused variance is smaller than both inputs: information never hurts.
