# A signal in the noise: the BBP transition

Plant one direction with variance $1 + \ell$ among $p - 1$ directions with variance 1. Does the top sample eigenvalue reveal it? Baik, Ben Arous and Péché found a sharp threshold (Section 6): if $\ell \le \sqrt\gamma$ the planted eigenvalue disappears into the bulk, and the top eigenvalue sits at the edge $(1 + \sqrt\gamma)^2$; if $\ell > \sqrt\gamma$ it separates, at $(1 + \ell)(1 + \gamma/\ell)$, and the top eigenvector's squared overlap with the planted direction tends to $\frac{1 - \gamma/\ell^2}{1 + \gamma/\ell}$.

- `spiked_samples(n, p, ell, rng)`: $n \times p$ standard normals with the first column multiplied by $\sqrt{1 + \ell}$.
- `top_eig_and_overlap(X)`: the largest eigenvalue of $X^\top X/n$ and the squared first entry of its eigenvector.
- `bbp_top(ell, gamma)` and `bbp_overlap(ell, gamma)`: the predictions (the edge and 0 below the threshold).

The tests run below and above the threshold with 800 samples of 200 features, $\gamma = 1/4$, and find the predictions within a few percent: the formulas are limits, and finite matrices fluctuate around them.

## Hints

1. `np.linalg.eigh` returns eigenvalues ascending and eigenvectors as columns; take the last.
2. The threshold $\sqrt\gamma$ means more samples per feature (smaller $\gamma$) reveal weaker signals.
3. Below the threshold the top eigenvector is a random direction: its overlap with any fixed direction is about $1/p$.
