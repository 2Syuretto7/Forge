import sub

base = "the quick brown fox jumps over the lazy dog while the cat sleeps in the warm sun"


def test_clean():
    docs = [base, base.upper(), "  " + base.replace(" ", "  "), "short text", "1234 5678 9012 " * 10, base + " again"]
    assert sub.clean(docs) == [0, 5]


def test_contaminated():
    train = [base, "a completely different text about something else entirely here and there"]
    test = ["a new sentence. " + " ".join(base.split()[3:12]), "nothing shared with training at all in this one", base.upper()]
    assert sub.contaminated(train, test) == [0, 2]
    assert sub.contaminated(train, test, n=12) == [2]
