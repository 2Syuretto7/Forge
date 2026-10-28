# Break it: strings that trip tokenizers

Training, encoding and decoding are provided.

1. `roundtrips(text, merges)`: whether `decode(encode(text))` gives back `text` exactly.
2. `normalization_forms(text)`: the NFC (composed) and NFD (decomposed) Unicode forms of `text`, using `unicodedata.normalize`.
3. `token_counts(texts, merges)`: the number of tokens of each text.

The tests show that "café" can be written two ways that look identical but are different bytes and different tokens, and that a leading space changes how a word is tokenized.

## Hints

1. `unicodedata.normalize("NFD", "é")` is "e" followed by a combining accent.
2. Byte-level BPE always round-trips; normalization is a choice you make before tokenizing.
3. Compare `token_counts(["the", " the"])` after training on text where " the" is common.
