def words_of(doc):
    """Lowercased words with surrounding punctuation stripped, empty ones dropped."""
    raise NotImplementedError


def ngrams(words, n=13):
    """The set of n-word tuples of a word list."""
    raise NotImplementedError


def build_index(eval_docs, n=13):
    """Every n-gram of every evaluation document."""
    raise NotImplementedError


def decontaminate(train_docs, eval_docs, n=13):
    """Indices of the training documents that share no n-gram with any evaluation document."""
    raise NotImplementedError
