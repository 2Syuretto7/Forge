# Capstone: compress embeddings, check the derivations

The starter's `make_embeddings(seed=0)` returns 100 embedding vectors in 2,048 dimensions, and `matmul_blocked(A, B, block=256)` computes $AB$ as a sum of products of 256-wide slices along the inner dimension: M33's blocking, which in the browser is several times faster than one large product. Use it for every product below.

1. `jl_project(X, k, seed=0)`: $XR$ with `R = np.random.default_rng(seed).standard_normal((d, k)) / sqrt(k)`.
2. `pairwise_dists(X)`: the distances $\lVert x_i - x_j\rVert$ for all pairs $i < j$, in `np.triu_indices` order, from the Gram matrix.
3. `max_distortion(X, Y)`: the largest $\left\lvert\frac{\lVert y_i - y_j\rVert}{\lVert x_i - x_j\rVert} - 1\right\rvert$ over all pairs, on distances, not squared distances.
4. `smallest_k(X, ks, tol=0.1, seed=0)`: the smallest $k$ in `ks` whose projection keeps every distance within `tol`, or `None`; compute the original distances once.
5. `jl_bound_k(n, eps)`: e04's $k$; for distances within 10 percent, use $\varepsilon = 0.19$ on squared distances, since $0.9^2 = 0.81$ and $1.1^2 = 1.21$.
6. `attention_check(ds=(16, 256, 1024), n=4000, seed=0)`: a dict from each $d$ to the variance of $q\cdot k/\sqrt d$ for standard normal $q, k$.
7. `init_check(L=50, width=128, seed=0)`: the ratio of the last layer's activation mean square to the first's under He initialization, as in e14.
8. `REPORT`: at least 120 words. Give the $k$ you chose and its measured worst distortion, compare it with the lemma's $k$, report the attention and initialization checks, and explain why the lemma's $k$ is larger than you needed.

The tests require every distance within 10 percent at the $k$ you choose (at most 1,024, half the original dimension), the attention variances within 0.1 of 1, and the initialization ratio between $\frac15$ and 5.
