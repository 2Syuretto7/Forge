import zlib
import numpy as np

DIM = 2 ** 12


def features(doc):
    """Hashed bag of lowercased words and word bigrams, scaled to unit length."""
    words = doc.lower().split()
    x = np.zeros(DIM)
    for t in words + [a + " " + b for a, b in zip(words, words[1:])]:
        x[zlib.crc32(t.encode("utf-8")) % DIM] += 1.0
    n = np.linalg.norm(x)
    return x / n if n else x


def loss_and_grad(w, b, X, y, l2):
    """Mean logistic loss of sigmoid(X w + b) against labels y in {0, 1}, plus l2 / 2 |w|^2.
    Return (loss, dw, db)."""
    raise NotImplementedError


def train(X, y, steps=300, lr=2.0, l2=1e-3):
    """Full-batch gradient descent from zero weights. Return (w, b)."""
    raise NotImplementedError
