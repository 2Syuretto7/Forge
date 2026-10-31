# Scale: 3,000 by 300, matrix-free ridge, a layer's kernels

::::predict{id=p4 kind=choice answer=c}
A $2000 \times 400$ matrix with geometrically decaying singular values. A rank-10 randomized SVD with oversampling 10 and one power iteration, against NumPy's full SVD, both in the browser. How much faster is the randomized one?

- It is slower: it makes four passes over the matrix.
- About the same.
- About ten times faster.
- About a thousand times faster.

:::reveal
About ten times (12 in the capstone's measurement in Pyodide, 16 in CPython), at an error within a hundredth of a percent of the optimum. The full SVD's cost grows like $mn^2$ whatever rank you want; the randomized one's like $mn(k + p)$, in products that run near peak. The gap widens as the matrix grows and the rank stays small.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

## The kernels of a layer

:::exercise{ref=e12}
:::
