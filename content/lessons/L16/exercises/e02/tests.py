import numpy as np
import sub


def text(words):
    return " ".join(words)


base = [f"word{i % 97}" for i in range(400)]
other = base[:300] + [f"other{i}" for i in range(100)]


def test_signature_shape_and_identity():
    a, b = sub.make_hashes(128, seed=1)
    s = sub.minhash(sub.shingle_ids({"abc", "bcd"}), a, b)
    assert s.shape == (128,) and np.all(s >= 0) and np.all(s < sub.PRIME)
    assert sub.estimate_jaccard(s, s) == 1.0


def test_minhash_estimates_jaccard():
    from_text = lambda t: {t[i:i + 5] for i in range(len(t) - 4)}
    A, B = from_text(text(base)), from_text(text(other))
    true = len(A & B) / len(A | B)
    a, b = sub.make_hashes(256, seed=3)
    est = sub.estimate_jaccard(sub.minhash(sub.shingle_ids(A), a, b), sub.minhash(sub.shingle_ids(B), a, b))
    assert abs(est - true) < 0.1
