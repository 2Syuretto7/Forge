import heapq
import math
from collections import Counter
import sub

TEXT = sub.CORPUS


def _optimal_lengths(probs):
    heap = [(p, i, 0) for i, p in enumerate(sorted(probs.values()))]
    heapq.heapify(heap)
    total = 0.0
    k = len(heap)
    while len(heap) > 1:
        p1, _, _ = heapq.heappop(heap)
        p2, _, _ = heapq.heappop(heap)
        total += p1 + p2  # each merge adds one bit to every symbol below it
        heapq.heappush(heap, (p1 + p2, k, 0))
        k += 1
    return total


def test_probabilities():
    p = sub.char_probs(TEXT)
    assert abs(sum(p.values()) - 1) < 1e-12
    assert abs(p[" "] - TEXT.count(" ") / len(TEXT)) < 1e-12


def test_code_is_prefix_free_and_complete():
    code = sub.huffman_code(sub.char_probs(TEXT))
    words = sorted(code.values())
    assert set(code) == set(TEXT)
    for a, b in zip(words, words[1:]):
        assert not b.startswith(a), f"{a} is a prefix of {b}"
    assert abs(sum(2 ** -len(w) for w in words) - 1) < 1e-12, "a Huffman code satisfies Kraft with equality"


def test_huffman_rate_is_optimal():
    probs = sub.char_probs(TEXT)
    code = sub.huffman_code(probs)
    expected = sum(probs[c] * len(code[c]) for c in probs)
    assert abs(expected - _optimal_lengths(probs)) < 1e-9
    assert abs(sub.bits_per_char(TEXT, code) - expected) < 1e-9


def test_round_trip():
    code = sub.huffman_code(sub.char_probs(TEXT))
    assert sub.decode(sub.encode(TEXT, code), code) == TEXT
    assert sub.huffman_code({"a": 1.0}) == {"a": "0"}


def test_entropy_bounds():
    code = sub.huffman_code(sub.char_probs(TEXT))
    h1 = sub.unigram_entropy(TEXT)
    rate = sub.bits_per_char(TEXT, code)
    assert h1 <= rate < h1 + 1
    c = Counter(TEXT)
    ref = -sum(k / len(TEXT) * math.log2(k / len(TEXT)) for k in c.values())
    assert abs(h1 - ref) < 1e-12
    h2 = sub.bigram_conditional_entropy(TEXT)
    assert 0 < h2 < h1 - 0.5


def test_report():
    words = sub.REPORT.split()
    assert len(words) >= 80, f"{len(words)} words"
    t = sub.REPORT.lower()
    assert "huffman" in t and "entropy" in t and "context" in t
