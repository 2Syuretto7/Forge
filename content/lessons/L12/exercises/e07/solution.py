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
    z = X @ w + b
    loss = np.mean(np.logaddexp(0, z) - y * z) + 0.5 * l2 * w @ w
    p = 1 / (1 + np.exp(-z))
    g = (p - y) / len(y)
    return loss, X.T @ g + l2 * w, g.sum()


def train(X, y, steps=300, lr=2.0, l2=1e-3):
    """Full-batch gradient descent from zero weights. Return (w, b)."""
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(steps):
        _, dw, db = loss_and_grad(w, b, X, y, l2)
        w -= lr * dw
        b -= lr * db
    return w, b
