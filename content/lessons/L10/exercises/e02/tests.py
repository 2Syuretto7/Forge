import sub

TEXT = "low lower lowest newer newest widest low lower newest " * 3


def test_first_merges():
    merges = sub.train_bpe(TEXT, 260)
    v = sub.vocab_bytes(merges)
    assert len(merges) == 4 and list(merges.values()) == [256, 257, 258, 259]
    first = list(merges)[0]
    ids = sub.to_bytes(TEXT)
    counts = sub.count_pairs(ids)
    assert counts[first] == max(counts.values())
    assert all(len(v[i]) >= 2 for i in range(256, 260))


def test_vocab_roundtrip_and_stop():
    merges = sub.train_bpe(TEXT, 400)
    v = sub.vocab_bytes(merges)
    assert len(merges) < 400 - 256
    for (a, b), i in merges.items():
        assert v[i] == v[a] + v[b]
    assert sub.train_bpe("abcdef", 300) == {}
