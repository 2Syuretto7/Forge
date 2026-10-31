# Concentration of measure: the norm of a random vector

A vector of $d$ independent standard normals has squared norm with mean $d$, but its norm concentrates sharply: its standard deviation stays near $1/\sqrt2$ however large $d$ is, so the relative spread $\operatorname{sd}(\lVert x\rVert)/\sqrt d$ shrinks like $1/\sqrt{2d}$ (Section 1). In high dimensions almost every random vector has nearly the same length, the fact behind M34's random matrices.

- `norms(d, samples, rng)`: the norms of `samples` random vectors in $\mathbb{R}^d$.
- `relative_spread(d, samples, rng)`: standard deviation of the norms over $\sqrt d$.
- `fraction_in_shell(d, samples, rng, width=0.1)`: the fraction of norms within $\pm$ `width` $\cdot\sqrt d$ of $\sqrt d$.

The tests check the constant standard deviation, the $1/\sqrt d$ relative spread, and that in 1,000 dimensions essentially every vector lies in the thin shell.

## Hints

1. `np.linalg.norm(rng.standard_normal((samples, d)), axis=1)`.
2. The squared norm is a sum of $d$ independent terms of variance 2; the delta method of M25 turns that into a standard deviation of about $1/\sqrt2$ for the norm.
3. Compare with $d = 1$, where the norm $\lvert x\rvert$ has standard deviation about $0.60$.
