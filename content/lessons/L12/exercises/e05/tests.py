import sub

FOOT = "Subscribe to our newsletter"
docs = [
    f"Story one.\n{FOOT}",
    f"story   ONE.\n{FOOT}",
    f"Story two.\n{FOOT}\n{FOOT}",
    "Story three.",
    f"Story four.\n{FOOT}",
]


def test_exact_dedup():
    assert sub.normalize("  A\n b ") == "a b"
    assert sub.exact_dedup(docs) == [0, 2, 3, 4]


def test_boilerplate():
    lines = sub.boilerplate_lines(docs, 3)
    assert lines == {FOOT}
    assert sub.boilerplate_lines(docs, 6) == set()
    assert sub.strip_lines(docs[2], lines) == "Story two."
    assert sub.strip_lines("a\n\nb", {"b"}) == "a\n"
