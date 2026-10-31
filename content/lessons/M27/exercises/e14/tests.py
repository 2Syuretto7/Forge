import sub

TEXT = sub.make_corpus(200000)
TRAIN, TEST = TEXT[:180000], TEXT[180000:]


def test_counts():
    full, ctx = sub.ngram_model("abab", 2)
    assert full["ab"] == 2 and full["ba"] == 1 and ctx["a"] == 2 and ctx["b"] == 1
    full, ctx = sub.ngram_model("aab", 1)
    assert full["a"] == 2 and ctx[""] == 3


def test_more_context_fewer_bits():
    t = sub.bits_table(TRAIN, TEST)
    assert 3.8 < t[1] < 4.3, t
    assert t[1] > t[2] > t[3] > t[4], t
    assert t[3] < 2.3 and t[4] < 1.8, t


def test_sparse_data_hurts_high_orders():
    small = sub.bits_table(TRAIN[:2000], TEST, orders=(3, 4))
    assert small[4] > small[3], small
