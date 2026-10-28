import re


def encode_train(text):
    """The encoding used to build the training data: UTF-8 bytes, unchanged."""
    return list(text.encode("utf-8"))


def encode_serve(text):
    """The serving front end's encoding: it tidies whitespace before encoding."""
    return list(re.sub(r"[ \t]+", " ", text).strip().encode("utf-8"))


def skew_report(samples):
    """Compare the two encodings on each sample. Return (rate, first) where rate is the fraction
    of samples whose token ids differ and first is (sample index, first differing position) for
    the first such sample, or None."""
    bad, first = 0, None
    for i, s in enumerate(samples):
        a, b = encode_train(s), encode_serve(s)
        if a != b:
            bad += 1
            if first is None:
                pos = next((j for j, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
                first = (i, pos)
    return bad / len(samples), first
