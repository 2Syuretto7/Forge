# The data stage

The first stage of the pipeline cleans the crawl and checks it against the evaluation set (L16). `normalize` and `ngrams` are provided.

1. `clean(docs, min_len=50, min_alpha=0.6)`: the indices of documents kept after exact deduplication on normalized text and two quality rules.
2. `contaminated(train_docs, test_docs, n=8)`: the indices of test documents sharing a word 8-gram with the training documents.

## Hints

1. Hash the normalized text with SHA-1 and keep a set of digests; a duplicate is dropped even if it would pass the rules.
2. The fraction of letters is the count of characters for which `str.isalpha` holds divided by the length.
3. Collect every training n-gram into one set, then test each test document against it.
