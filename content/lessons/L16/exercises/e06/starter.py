STOP_WORDS = {"the", "be", "to", "of", "and", "that", "have", "with"}


def quality_signals(doc):
    """Signals used by the Gopher quality rules, over whitespace-separated words and non-empty
    lines: n_words, mean_word_len, symbol_ratio (the larger of the counts of "#" and of "..." per
    word), bullet_lines (fraction starting with a bullet: "-", "*" or a bullet character after
    leading spaces), ellipsis_lines (fraction ending with "..."), alpha_words (fraction of words
    with a letter) and stop_words (how many STOP_WORDS occur, case-insensitive, punctuation
    stripped)."""
    raise NotImplementedError


def passes(doc, min_words=50, max_words=100000):
    """Gopher's rules: word count in [min_words, max_words], mean word length in [3, 10], symbol
    ratio at most 0.1, at most 90% bullet lines and 30% ellipsis lines, at least 80% of words with
    a letter, and at least two of the stop words."""
    raise NotImplementedError
