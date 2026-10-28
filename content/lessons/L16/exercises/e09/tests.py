import numpy as np
import sub

rng = np.random.default_rng(9)
VOCAB = [f"w{i}" for i in range(500)]


def doc(n=60):
    return " ".join(rng.choice(VOCAB, n))


evals = [doc() for _ in range(5)]
train = [doc() for _ in range(20)]
leak = " ".join(train[3].split()[:20]) + " " + evals[2].upper().replace(" ", ", ", 3) + " " + " ".join(train[4].split()[:10])
train.append(leak)


def test_ngrams():
    assert sub.words_of("The, cat (sat).") == ["the", "cat", "sat"]
    assert sub.ngrams(["a", "b", "c"], 2) == {("a", "b"), ("b", "c")}
    assert sub.ngrams(["a"], 2) == set()


def test_decontaminate():
    keep = sub.decontaminate(train, evals)
    assert keep == list(range(20))
    assert len(sub.build_index(evals)) == 5 * 48
