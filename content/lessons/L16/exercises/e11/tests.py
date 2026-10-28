import sub

train = sub.make_docs(300, seed=1)
evals = sub.make_docs(30, seed=2)
V = 401


def test_counts():
    ctx, full = sub.train_counts(["a b a b"], 2)
    assert ctx[("<s>",)] == 1 and ctx[("a",)] == 2 and ctx[("b",)] == 1
    assert full[("a", "b")] == 2 and full[("<s>", "a")] == 1


def score(n, docs, extra=()):
    return sub.avg_logloss(sub.train_counts(train + list(extra), n), docs, n, V, k=0.01)


def test_leak_inflates_the_score():
    clean, leaked = score(3, evals), score(3, evals, evals)
    assert leaked < 0.6 * clean
    # On documents that did not leak, the leaked model is no better.
    assert abs(score(3, sub.make_docs(30, seed=3), evals) - clean) < 0.15 * clean


def test_leak_reverses_model_selection():
    # The chain is first order: on clean evaluation the bigram model is best...
    assert score(2, evals) < score(4, evals)
    # ...but with the evaluation set in training, the memorizing 4-gram model looks best.
    assert score(4, evals, evals) < score(2, evals, evals)
