import sub

TEXT = "the cafe and the café; the theatre, the theme. " * 6


def test_roundtrip_edge_cases():
    merges = sub.train_bpe(TEXT, 320)
    for s in ["", " ", "\n\n", "  the  ", "café", "café", "東京で", "tab\there"]:
        assert sub.roundtrips(s, merges), repr(s)


def test_normalization_changes_bytes_and_tokens():
    nfc, nfd = sub.normalization_forms("café")
    assert nfc != nfd and len(nfc) == 4 and len(nfd) == 5
    merges = sub.train_bpe(TEXT, 320)
    a, b = sub.token_counts([nfc, nfd], merges)
    assert a != b


def test_leading_space_matters():
    merges = sub.train_bpe(TEXT, 320)
    with_space, without = sub.token_counts([" the", "the"], merges)
    assert with_space <= without
