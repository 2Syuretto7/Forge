# Capstone: a semantic search toy

The starter generates 20,000 embeddings in 48 dimensions, grouped by topic, and 20 queries. The reference answer is the exact top 5 by cosine similarity. Your search engine must find at least 90 percent of those neighbours while computing similarities with at most a quarter of the stored vectors, using an **inverted file index**: group the vectors around centroids, and for each query search only the groups whose centroids are most similar to it.

:::exercise{ref=capstone}
:::

## When you finish

You have built vector search, the retrieval step of most systems that look things up in embedding space. M10 turns your matrix-vector products into linear maps; M12 projects onto many directions at once; and in M34 the near-orthogonality of random directions, which made cosines of 0.06 meaningless in the puzzle, becomes a theorem.

:::edge{to=M34 text="near-orthogonality of random directions in high dimension, proved."}
:::
