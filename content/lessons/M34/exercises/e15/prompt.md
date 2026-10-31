# Break it: embeddings that are not random

The near-orthogonality of e02 holds for isotropic random vectors. Real embeddings are not isotropic: they often share a large common component, so the cosine between unrelated items is far from 0, and every "random direction" intuition breaks (Section 2). Centering, subtracting the mean vector, removes the shared component.

- `anisotropic(n, d, common, rng)`: rows $m + z_i$ with a fixed random mean direction $m$ of length `common` times $\sqrt d$ and standard normal $z_i$.
- `mean_pairwise_cosine(X)`: the average cosine over all pairs $i < j$.
- `center(X)`: subtract the mean row.
- `predicted_cosine(common)`: $\frac{c^2}{c^2 + 1}$ for `common` $= c$, from $\lVert m\rVert^2 = c^2d$ against $\mathbb{E}\lVert z\rVert^2 = d$.

The tests find a mean cosine of about $\frac12$ between unrelated rows with $c = 1$, and about 0 after centering.

## Hints

1. Normalize the rows, form the Gram matrix, and average its strictly upper triangle.
2. For large $d$ the cosine is $\frac{(m + z_i)\cdot(m + z_j)}{\lVert m + z_i\rVert\lVert m + z_j\rVert} \approx \frac{\lVert m\rVert^2}{\lVert m\rVert^2 + d}$.
3. Language-model embeddings are known to occupy a narrow cone; centering and whitening are common fixes before using cosine similarity.
