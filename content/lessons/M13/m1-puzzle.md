# Puzzle: the direction that wins

Take $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ and a random starting vector. Multiply by $A$, rescale to length 1, and repeat fifty times.

::::predict{id=p1 kind=choice answer=a}
Where does the direction end up?

- Along $(1, 1)$, whatever the start (unless the start is exactly along $(1, -1)$).
- Wherever it started: $A$ only stretches.
- It keeps rotating forever.
- Along $(1, 0)$, the first column's direction.

:::reveal
Along $(1, 1)$. $A$ sends $(1, 1)$ to $(3, 3)$, three times itself, and $(1, -1)$ to $(1, -1)$, unchanged. Any start is a mix of the two, and each multiplication triples the first part while leaving the second alone, so after fifty steps the first part dominates by a factor of $3^{50}$. A start exactly along $(1, -1)$ never acquires any $(1, 1)$ part, which is why random starts are used.
:::
::::

::::predict{id=p2 kind=numeric answer=0.333 tol=0.01}
By what factor does the ratio (part along $(1, -1)$) / (part along $(1, 1)$) shrink at each step?

:::reveal
$1/3$: the ratio of the two stretch factors, the **eigenvalues** 1 and 3. After 10 steps it has shrunk by $3^{-10} \approx 1.7 \times 10^{-5}$. The second eigenvalue over the first sets the speed of everything in this lesson, from PageRank to Markov chains.
:::
::::

Start from any direction and step $k$ up. The dashed lines are the two kept directions. Try the other matrices: one has no kept direction, one has only one, and one has two that pull equally hard.

:::widget{name=EigenFlow preset=sym steps=6}
:::

## Questions to carry into the derivation

1. How do you find the directions a matrix keeps, and the factors?
2. When does a matrix have enough of them to describe it completely?
3. Why are the kept directions of a symmetric matrix perpendicular?
4. What does the winning direction mean for a random walk on the web?
