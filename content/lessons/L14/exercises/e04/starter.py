def to_bytes(text):
    """The UTF-8 bytes of text, as a list of integers 0..255."""
    return list(text.encode("utf-8"))


def from_bytes(ids):
    """Decode a list of byte values back to text, replacing invalid sequences."""
    return bytes(ids).decode("utf-8", errors="replace")


def count_pairs(ids, counts=None):
    """Counts of adjacent pairs, in order of first occurrence."""
    counts = {} if counts is None else counts
    for a, b in zip(ids, ids[1:]):
        counts[(a, b)] = counts.get((a, b), 0) + 1
    return counts


def merge(ids, pair, new_id):
    """Replace every non-overlapping occurrence of pair, scanning left to right, with new_id."""
    out, i = [], 0
    while i < len(ids):
        if i + 1 < len(ids) and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            out.append(new_id)
            i += 2
        else:
            out.append(ids[i])
            i += 1
    return out

import re

# A simplified version of GPT-2's pattern: contractions, words and numbers with an optional leading
# space, runs of punctuation with an optional leading space, and whitespace.
PATTERN = re.compile(r"'s|'t|'re|'ve|'m|'ll|'d| ?[^\W\d_]+| ?\d+| ?[^\s\w]+|\s+(?!\S)|\s+")


def pretokenize(text):
    """Split text into chunks with PATTERN; the chunks concatenate back to text exactly."""
    raise NotImplementedError


def train_bpe_chunks(text, vocab_size):
    """Byte-level BPE where pairs are counted within chunks only, so no merge crosses a chunk
    boundary. Count each distinct chunk once, weighted by how often it occurs."""
    raise NotImplementedError
