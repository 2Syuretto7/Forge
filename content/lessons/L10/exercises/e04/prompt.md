# Pre-tokenization

`PATTERN` is a simplified version of GPT-2's splitting rule: contractions, words and numbers with an optional leading space, runs of punctuation with an optional leading space, and whitespace.

1. `pretokenize(text)`: the list of chunks `PATTERN.findall(text)`, which concatenate back to `text`.
2. `train_bpe_chunks(text, vocab_size)`: BPE in which pairs are counted only inside chunks, so no merge crosses a chunk boundary. Count each distinct chunk once with its frequency, which also makes training much faster.

## Hints

1. Build `freq = {chunk: count}` and `words = {chunk: list of byte ids}`.
2. Each round, add `freq[chunk]` for every adjacent pair inside each chunk's ids.
3. Apply the chosen merge to every chunk's ids.
