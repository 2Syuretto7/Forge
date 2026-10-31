# Exact duplicates and boilerplate

Before near-duplicates, the cheap wins: identical documents and lines repeated across many pages (navigation menus, cookie notices, licence footers).

1. `normalize(doc)`: lowercase and collapse whitespace.
2. `exact_dedup(docs)`: the indices of the first occurrence of each document, comparing SHA-1 digests of the normalized text.
3. `boilerplate_lines(docs, min_docs)`: the set of stripped, non-empty lines that occur in at least `min_docs` different documents (count each line once per document).
4. `strip_lines(doc, lines)`: the document without the lines whose stripped text is in `lines`.

## Hints

1. `hashlib.sha1(s.encode("utf-8")).hexdigest()` gives a fixed-size key; storing digests instead of documents keeps memory small.
2. Count lines through a per-document set so that a line repeated within one document counts once.
3. Keep blank lines in `strip_lines`; only remove the listed ones.
