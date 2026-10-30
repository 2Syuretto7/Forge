# Samplers built from uniform random numbers

Every sampler can be built from uniform numbers on $[0, 1)$ (Section 5). Each function receives the uniforms it needs, so results are deterministic and testable.

- `sample_categorical(probs, u)`: for each `u[i]`, return the index of the interval of $[0,1)$ it falls in when the interval is split into pieces of lengths `probs`. Integer array, same shape as `u`.
- `sample_exponential(lam, u)`: inverse-CDF sampling, $x = -\log(1 - u)/\lambda$.
- `box_muller(u1, u2)`: two arrays of standard normal samples, $z_1 = \sqrt{-2\log u_1}\cos(2\pi u_2)$ and $z_2 = \sqrt{-2\log u_1}\sin(2\pi u_2)$. Return `(z1, z2)`.

## Hints

1. `np.searchsorted(np.cumsum(probs), u, side="right")` finds the interval index.
2. Clip the result to `len(probs) - 1` in case rounding makes the cumulative sum slightly below 1.
3. Box-Muller needs $u_1 > 0$; the tests never pass exactly 0.
