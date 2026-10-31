# Encoding and decoding

Training is provided. Implement:

1. `encode(text, merges)`: take the bytes of `text`, then repeatedly find, among the adjacent pairs present, the one learned earliest (the smallest new id), and merge it; stop when no present pair has been learned.
2. `decode(ids, merges)`: concatenate the byte strings of the ids and decode as UTF-8 (replacing invalid sequences).

Encoding the training text must give the same ids as the training loop produced, and decoding must invert encoding for any string, including characters never seen in training.

## Hints

1. `min(pairs, key=lambda p: merges.get(p, float("inf")))`.
2. If the best pair has rank infinity, no learned merge applies.
3. `vocab_bytes(merges)` (provided) gives every id's bytes.
