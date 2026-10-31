# Locality-sensitive hashing: the S-curve

Split each signature of $b \cdot r$ values into $b$ **bands** of $r$ rows and put two documents in the same bucket if any band matches exactly. Two documents with Jaccard similarity $s$ agree on one band with probability $s^r$, so they become **candidates** with probability
$$
P(s) = 1 - (1 - s^r)^b.
$$

1. `candidate_probability(s, bands, rows)`.
2. `dprob_ds(s, bands, rows)`: its derivative with respect to $s$.
3. `threshold(bands, rows)`: $(1/b)^{1/r}$, the approximate similarity where the curve rises steeply.
4. `choose_bands(num_perm, target)`: among the factorizations $b \cdot r$ = `num_perm`, the one whose threshold is closest to `target`.

## Hints

1. By the chain rule, $P'(s) = b\,r\,s^{r-1}(1 - s^r)^{b-1}$.
2. More rows per band make the curve steeper and move it right; more bands move it left.
3. At the threshold, $s^r = 1/b$, so $P = 1 - (1 - 1/b)^b \approx 1 - 1/e$ for large $b$.
