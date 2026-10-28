def shingles(text, k=5):
    """The set of character k-grams of text, lowercased and with whitespace runs collapsed to a
    single space. A text shorter than k is its own single shingle."""
    t = " ".join(text.lower().split())
    return {t[i:i + k] for i in range(len(t) - k + 1)} if len(t) >= k else {t}


def jaccard(a, b):
    """|a and b| / |a or b| for two sets; 1.0 if both are empty."""
    return len(a & b) / len(a | b) if (a or b) else 1.0
