import hashlib


def normalize(doc):
    return " ".join(doc.lower().split())


def ngrams(text, n):
    w = text.lower().split()
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def clean(docs, min_len=50, min_alpha=0.6):
    """Indices of the documents kept: drop every document whose normalized text was seen
    before, then those shorter than min_len characters or with a fraction of letters below
    min_alpha."""
    raise NotImplementedError


def contaminated(train_docs, test_docs, n=8):
    """Indices of the test documents that share at least one word n-gram with the training
    documents."""
    raise NotImplementedError
