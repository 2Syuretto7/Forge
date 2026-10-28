import hashlib


def normalize(doc):
    """Lowercase and collapse whitespace runs to single spaces."""
    raise NotImplementedError


def exact_dedup(docs):
    """Indices of the first occurrence of each document, comparing SHA-1 digests of the normalized
    text."""
    raise NotImplementedError


def boilerplate_lines(docs, min_docs):
    """The set of stripped, non-empty lines that occur in at least min_docs different documents."""
    raise NotImplementedError


def strip_lines(doc, lines):
    """doc without the lines whose stripped text is in `lines`."""
    raise NotImplementedError
