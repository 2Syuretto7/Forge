import sub

TEXT = "the cat sat on the mat; the cat ate the rat. " * 4


def test_roundtrip():
    merges = sub.train_bpe(TEXT, 300)
    for s in [TEXT, "the theme", "naïve 東京!", "", "   "]:
        assert sub.decode(sub.encode(s, merges), merges) == s


def test_compresses_training_text():
    merges = sub.train_bpe(TEXT, 300)
    ids = sub.encode(TEXT, merges)
    assert len(ids) < len(TEXT.encode()) / 3
    assert all(i < 300 for i in ids)
