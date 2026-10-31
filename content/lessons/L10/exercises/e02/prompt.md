# Training a BPE vocabulary

Your byte helpers are provided.

1. `train_bpe(text, vocab_size)`: start from the bytes of `text`; for each new id $256, 257, \dots$ up to `vocab_size - 1`, count pairs, pick the most frequent (ties go to the pair seen first), stop early if no pair occurs at least twice, merge it into the new id, and record the merge. Return `{(a, b): new_id}` in the order learned.
2. `vocab_bytes(merges)`: the byte string of every id, built from the 256 single bytes by concatenating the two parts of each merge.

## Hints

1. `max(counts, key=counts.get)` returns the first key with the largest count.
2. Merges must be learned on the sequence produced by the previous merges.
3. Later merges can combine earlier ones: the byte string of a merged id is the concatenation of its parts' byte strings.
