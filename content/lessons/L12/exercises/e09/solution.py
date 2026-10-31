def words_of(doc):
    """Lowercased words with surrounding punctuation stripped, empty ones dropped."""
    out = [w.strip(".,;:!?\"'()[]").lower() for w in doc.split()]
    return [w for w in out if w]


def ngrams(words, n=13):
    """The set of n-word tuples of a word list."""
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


def build_index(eval_docs, n=13):
    """Every n-gram of every evaluation document."""
    index = set()
    for d in eval_docs:
        index |= ngrams(words_of(d), n)
    return index


def decontaminate(train_docs, eval_docs, n=13):
    """Indices of the training documents that share no n-gram with any evaluation document."""
    index = build_index(eval_docs, n)
    return [i for i, d in enumerate(train_docs) if not (ngrams(words_of(d), n) & index)]
