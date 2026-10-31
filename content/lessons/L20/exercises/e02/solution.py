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
    seen, keep = set(), []
    for i, d in enumerate(docs):
        h = hashlib.sha1(normalize(d).encode("utf-8")).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        if len(d) < min_len or sum(c.isalpha() for c in d) / len(d) < min_alpha:
            continue
        keep.append(i)
    return keep


def contaminated(train_docs, test_docs, n=8):
    """Indices of the test documents that share at least one word n-gram with the training
    documents."""
    grams = set()
    for d in train_docs:
        grams |= ngrams(d, n)
    return [i for i, d in enumerate(test_docs) if ngrams(d, n) & grams]
