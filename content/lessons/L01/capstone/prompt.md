# Capstone: a PCA pipeline for an embedding set

You receive a synthetic embedding set: 1,500 points in 48 dimensions. The dimensions come in six named groups of eight (`science_0` to `science_7`, then `finance`, `music`, `sports`, `politics`, `travel`). The generator is in the starter; do not change it.

Build the pipeline and interpret it:

1. `fit_pca(X)` returns `(mean, components, ratios)`: the mean `(d,)`, **all** principal directions as rows `(d, d)` with the sign convention from exercise 11 (largest-magnitude entry positive), and the explained variance ratios `(d,)`, descending.
2. `k_for_variance(ratios, target)` returns the smallest `k` whose cumulative ratio reaches `target`.
3. `reconstruct(X, mean, components, k)` projects onto the top `k` directions and maps back to the original space, shape `(n, d)`.
4. `top_groups(components, names, top)` returns, for each of the first `top` components, the name of the group (the part of the feature name before the underscore) that holds the largest share of that component's squared loadings.
5. `REPORT`: a written interpretation of at least 80 words. Say how many components reach 95 percent of the variance, what each of the top three components measures in terms of the feature groups, and what the remaining components mostly contain.

The tests check the numbers, the reconstruction identity $\|X_c - \hat X_c\|_F^2 / \|X_c\|_F^2 = 1 - \sum_{i \le k} r_i$, the group assignment, and that the report names the groups you found.
