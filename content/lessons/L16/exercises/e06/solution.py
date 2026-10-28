STOP_WORDS = {"the", "be", "to", "of", "and", "that", "have", "with"}


def quality_signals(doc):
    """Signals used by the Gopher quality rules, over whitespace-separated words and non-empty
    lines: n_words, mean_word_len, symbol_ratio (the larger of the counts of "#" and of "..." per
    word), bullet_lines (fraction starting with a bullet: "-", "*" or a bullet character after
    leading spaces), ellipsis_lines (fraction ending with "..."), alpha_words (fraction of words
    with a letter) and stop_words (how many STOP_WORDS occur, case-insensitive, punctuation
    stripped)."""
    words = doc.split()
    lines = [l for l in doc.split("\n") if l.strip()]
    n = max(1, len(words))
    m = max(1, len(lines))
    found = {w.strip(".,;:!?\"'()").lower() for w in words} & STOP_WORDS
    return {
        "n_words": len(words),
        "mean_word_len": sum(len(w) for w in words) / n,
        "symbol_ratio": max(doc.count("#"), doc.count("...")) / n,
        "bullet_lines": sum(l.lstrip()[:1] in ("-", "*", "\u2022") for l in lines) / m,
        "ellipsis_lines": sum(l.rstrip().endswith("...") for l in lines) / m,
        "alpha_words": sum(any(c.isalpha() for c in w) for w in words) / n,
        "stop_words": len(found),
    }


def passes(doc, min_words=50, max_words=100000):
    """Gopher's rules: word count in [min_words, max_words], mean word length in [3, 10], symbol
    ratio at most 0.1, at most 90% bullet lines and 30% ellipsis lines, at least 80% of words with
    a letter, and at least two of the stop words."""
    s = quality_signals(doc)
    return (
        min_words <= s["n_words"] <= max_words
        and 3 <= s["mean_word_len"] <= 10
        and s["symbol_ratio"] <= 0.1
        and s["bullet_lines"] <= 0.9
        and s["ellipsis_lines"] <= 0.3
        and s["alpha_words"] >= 0.8
        and s["stop_words"] >= 2
    )
