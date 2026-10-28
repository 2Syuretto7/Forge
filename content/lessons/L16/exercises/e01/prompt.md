# Shingles and Jaccard similarity

Near-duplicate detection compares documents as sets of short overlapping pieces.

1. `shingles(text, k=5)`: the set of character $k$-grams of `text` after lowercasing and collapsing every run of whitespace to a single space. A text shorter than $k$ is its own single shingle.
2. `jaccard(a, b)`: $|a \cap b| / |a \cup b|$, and 1.0 when both sets are empty.

## Hints

1. `" ".join(text.lower().split())` normalizes case and whitespace in one line.
2. A set comprehension over `range(len(t) - k + 1)` collects the $k$-grams.
3. Two copies of a page that differ only in spacing or capitalization have Jaccard similarity 1.
