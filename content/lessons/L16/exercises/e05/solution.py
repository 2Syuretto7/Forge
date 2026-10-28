import hashlib


def normalize(doc):
    """Lowercase and collapse whitespace runs to single spaces."""
    return " ".join(doc.lower().split())


def exact_dedup(docs):
    """Indices of the first occurrence of each document, comparing SHA-1 digests of the normalized
    text."""
    seen, keep = set(), []
    for i, d in enumerate(docs):
        h = hashlib.sha1(normalize(d).encode("utf-8")).hexdigest()
        if h not in seen:
            seen.add(h)
            keep.append(i)
    return keep


def boilerplate_lines(docs, min_docs):
    """The set of stripped, non-empty lines that occur in at least min_docs different documents."""
    counts = {}
    for d in docs:
        for line in {l.strip() for l in d.split("\n") if l.strip()}:
            counts[line] = counts.get(line, 0) + 1
    return {line for line, c in counts.items() if c >= min_docs}


def strip_lines(doc, lines):
    """doc without the lines whose stripped text is in `lines`."""
    return "\n".join(l for l in doc.split("\n") if l.strip() not in lines)
