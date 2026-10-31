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


def train_bpe(text, vocab_size):
    """Byte-level BPE: start from the 256 byte values and repeatedly merge the most frequent adjacent
    pair (ties: the pair seen first) into a new id 256, 257, ... until vocab_size ids exist or no pair
    occurs twice. Return the merges as a dict {(a, b): new_id} in the order they were learned."""
    ids = to_bytes(text)
    merges = {}
    for new_id in range(256, vocab_size):
        counts = count_pairs(ids)
        if not counts:
            break
        best = max(counts, key=counts.get)
        if counts[best] < 2:
            break
        ids = merge(ids, best, new_id)
        merges[best] = new_id
    return merges


def vocab_bytes(merges):
    """The byte string each id stands for."""
    vocab = {i: bytes([i]) for i in range(256)}
    for (a, b), i in merges.items():
        vocab[i] = vocab[a] + vocab[b]
    return vocab
