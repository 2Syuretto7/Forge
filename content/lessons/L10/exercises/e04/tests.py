import sub

TEXT = "Hello world. It's the world's end; the end of the world, hello again.\n\n  Hello!" * 5


def test_chunks():
    chunks = sub.pretokenize(TEXT)
    assert "".join(chunks) == TEXT
    assert " world" in chunks and "'s" in chunks
    assert sub.pretokenize("a  b") == ["a", " ", " b"]


def test_no_merge_crosses_a_word_boundary():
    merges = sub.train_bpe_chunks(TEXT, 330)
    v = {i: bytes([i]) for i in range(256)}
    for (a, b), i in merges.items():
        v[i] = v[a] + v[b]
    for i in range(256, 256 + len(merges)):
        s = v[i].decode("utf-8", errors="ignore")
        # spaces attach to the following word, so no token has a visible character before a space
        assert not any(not c.isspace() and n == " " for c, n in zip(s, s[1:])), s
    assert any(v[i] == b" world" for i in v)
