import math
import re
from collections import Counter

import numpy as np

# provided
WORDS = (
    "the old harbor town wakes before the sun fishermen check their nets by lamplight and the baker on the corner "
    "pulls the first loaves from an oven that has been warm since midnight by six the tide has turned and the boats "
    "slip out one by one past the lighthouse whose keeper waves from the gallery as he has every morning for thirty "
    "years in the market the stalls open slowly a woman arranges lemons in a careful pyramid a boy carries ice to the "
    "fish sellers and the clock mender unlocks his narrow shop where a hundred clocks disagree about the time visitors "
    "arrive with the second ferry they walk the sea wall photograph the boats and ask the same questions about the "
    "weather which the locals answer patiently and differently every time at noon the bells ring and the town eats "
    "bread fish olives and whatever the morning offered in the afternoon the wind rises the boats come back heavy or "
    "light and the gulls follow every crate an old dog sleeps in the only patch of sun undisturbed by the noise when "
    "the light goes the lamps come on along the harbor and the reflections stretch and break on the moving water"
).split()


# provided
def make_corpus(n_chars, seed=0):
    freq = Counter(WORDS)
    vocab = sorted(freq)
    p = np.array([freq[w] for w in vocab], dtype=float)
    p /= p.sum()
    rng = np.random.default_rng(seed)
    out, n = [], 0
    while n < n_chars:
        k = int(rng.integers(4, 16))
        sentence = " ".join(vocab[i] for i in rng.choice(len(vocab), size=k, p=p)) + ". "
        out.append(sentence)
        n += len(sentence)
    return "".join(out)[:n_chars]


def ngram_model(text, n):
    """Counts of n-grams and of their (n-1)-character contexts."""
    raise NotImplementedError


def cross_entropy_bits(train, test, n, k=0.1):
    """Held-out bits per character of an add-k smoothed n-gram model."""
    raise NotImplementedError


def bits_table(train, test, orders=(1, 2, 3, 4)):
    """Cross-entropy in bits per character for each order."""
    raise NotImplementedError
