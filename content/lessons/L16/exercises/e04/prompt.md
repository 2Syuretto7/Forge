# Deduplicating with LSH

You have one MinHash signature per document (an array of `bands * rows` integers).

1. `lsh_candidates(signatures, bands, rows)`: put each band of each signature in a bucket keyed by (band index, tuple of the band's values), and return the sorted list of pairs $(i, j)$, $i < j$, that share at least one bucket.
2. `dedup_keep(signatures, bands, rows, min_similarity)`: confirm each candidate pair by its signature agreement rate, join confirmed pairs into clusters with union-find, and return the sorted indices to keep, the smallest index of every cluster.

## Hints

1. A dictionary from bucket key to the list of document indices builds the buckets in one pass.
2. Candidates are cheap but approximate: confirming them with the full signature removes most false positives.
3. Union-find: each index points to a parent; `find` follows parents to the root, and joining two clusters points one root at the other (point the larger root at the smaller to keep the smallest index as the root).
