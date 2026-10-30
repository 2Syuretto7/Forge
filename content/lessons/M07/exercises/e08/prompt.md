# Euler's formula from the series

- `exp_series(z, terms=40)`: $\sum_{k=0}^{\text{terms}-1} z^k / k!$ for a Python complex number `z`, building each term from the previous one.
- `euler_gap(theta)`: the distance $|e^{i\theta} - (\cos\theta + i\sin\theta)|$ with $e^{i\theta}$ from your series.
- `real_and_imaginary_terms(theta, terms=20)`: the pair of lists of the real and imaginary parts of the series terms for $z = i\theta$. The real parts are the terms of the cosine series $1 - \theta^2/2! + \theta^4/4! - \dots$ (with zeros in between); the imaginary parts are those of the sine series.

The tests confirm $e^{i\pi} = -1$ to within $10^{-12}$.

## Hints

1. `term *= z / k`.
2. `abs(exp_series(1j * theta) - complex(math.cos(theta), math.sin(theta)))`.
3. Build the list of terms, then take `.real` and `.imag` of each.
