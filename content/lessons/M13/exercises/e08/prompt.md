# PageRank on a handful of pages

`links` is a list of `(src, dst)` pairs among pages `0` to `n - 1`.

- `google_matrix(links, n, d=0.85)`: the dense column-stochastic matrix of the random surfer: with probability `d` follow one of the current page's links uniformly at random (a page with no links jumps to a uniformly random page instead), and with probability `1 - d` jump to a uniformly random page.
- `pagerank(links, n, d=0.85, tol=1e-12)`: its stationary distribution by power iteration from the uniform distribution.

## Hints

1. Column `j` of the link part is $1/\text{outdeg}(j)$ at each target of `j`, or $1/n$ everywhere if `j` has no links.
2. $G = d\,S + (1 - d)/n$ in every entry.
3. Repeated links count twice, like two links.
