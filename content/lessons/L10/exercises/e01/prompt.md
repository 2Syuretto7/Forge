# Bytes, pairs and one merge

1. `to_bytes(text)`: the UTF-8 bytes of `text` as a list of integers.
2. `from_bytes(ids)`: decode a list of byte values to text, replacing invalid sequences.
3. `count_pairs(ids, counts=None)`: a dictionary from each adjacent pair to its count, in order of first occurrence (add to `counts` if one is given).
4. `merge(ids, pair, new_id)`: replace every occurrence of `pair`, scanning left to right without overlaps, by `new_id`.

## Hints

1. `text.encode("utf-8")` is a `bytes` object; `list(...)` gives the integers.
2. `bytes(ids).decode("utf-8", errors="replace")`.
3. In `merge`, advance by two positions after a replacement and by one otherwise.
