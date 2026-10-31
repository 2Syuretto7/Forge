import sub


def test_shingles():
    assert sub.shingles("abcdef", 3) == {"abc", "bcd", "cde", "def"}
    assert sub.shingles("Ab  C", 2) == {"ab", "b ", " c"}
    assert sub.shingles("hi", 5) == {"hi"}


def test_jaccard():
    a = sub.shingles("the cat sat on the mat")
    assert sub.jaccard(a, a) == 1.0
    assert sub.jaccard(a, sub.shingles("THE  cat sat on the mat")) == 1.0
    assert sub.jaccard({"x"}, {"y"}) == 0.0
    assert sub.jaccard({1, 2, 3}, {2, 3, 4}) == 0.5
    assert sub.jaccard(set(), set()) == 1.0
