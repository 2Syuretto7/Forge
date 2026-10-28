# MinHash signatures

Comparing every pair of documents' shingle sets is quadratic in the corpus and slow for each pair. MinHash compresses each set into a short signature whose agreement rate estimates the Jaccard similarity. `make_hashes(num_perm, seed)` gives the coefficients of hash functions $h_i(x) = (a_i x + b_i) \bmod p$ with $p = 2^{31} - 1$, and `shingle_ids` maps shingles to integers.

1. `minhash(ids, a, b)`: for each hash function, the minimum of $h_i(x)$ over the shingle ids (reduced mod $p$ first).
2. `estimate_jaccard(sig1, sig2)`: the fraction of positions where two signatures agree.

## Hints

1. `np.outer(a, x) + b[:, None]` evaluates every hash function on every shingle at once; reduce mod `PRIME` and take the minimum along axis 1.
2. Use 64-bit integers: $a x + b < 2^{62}$ fits.
3. For one random hash, the minimum over $A \cup B$ lands in $A \cap B$ with probability $|A \cap B| / |A \cup B|$, and then both minima are equal.
