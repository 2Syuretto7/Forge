def shingles(text, k=5):
    """The set of character k-grams of text, lowercased and with whitespace runs collapsed to a
    single space. A text shorter than k is its own single shingle."""
    raise NotImplementedError


def jaccard(a, b):
    """|a and b| / |a or b| for two sets; 1.0 if both are empty."""
    raise NotImplementedError
