import sub


def test_bytes_roundtrip():
    for s in ["hello", "naïve café", "東京", ""]:
        b = sub.to_bytes(s)
        assert all(0 <= v < 256 for v in b) and sub.from_bytes(b) == s
    assert len(sub.to_bytes("é")) == 2 and len(sub.to_bytes("東")) == 3


def test_pairs_and_merge():
    ids = sub.to_bytes("aaabdaaabac")
    c = sub.count_pairs(ids)
    a, b = ord("a"), ord("b")
    assert c[(a, a)] == 4 and c[(a, b)] == 2 and list(c)[0] == (a, a)
    m = sub.merge(ids, (a, a), 256)
    assert len(m) == 9 and m[:3] == [256, a, b]
    assert sub.merge([1, 1, 1], (1, 1), 9) == [9, 1]
