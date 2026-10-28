# Quality heuristics

Rae et al. (2021) filtered web text for Gopher with simple rules. Implement them.

1. `quality_signals(doc)` returning a dictionary with:
   - `n_words`: whitespace-separated words;
   - `mean_word_len`;
   - `symbol_ratio`: the larger of the number of `#` characters and of `...` occurrences, per word;
   - `bullet_lines`: the fraction of non-empty lines starting (after leading spaces) with `-`, `*` or a bullet character (`"•"`);
   - `ellipsis_lines`: the fraction of non-empty lines ending with `...`;
   - `alpha_words`: the fraction of words containing at least one letter;
   - `stop_words`: how many of `STOP_WORDS` occur (case-insensitive, with surrounding punctuation stripped).
2. `passes(doc, min_words=50, max_words=100000)`: between `min_words` and `max_words` words, mean word length between 3 and 10, symbol ratio at most 0.1, at most 90% bullet lines and 30% ellipsis lines, at least 80% of words with a letter, and at least two stop words.

## Hints

1. Guard every ratio against empty documents with `max(1, ...)` in the denominator.
2. `any(c.isalpha() for c in w)` tests a word for a letter.
3. The stop-word rule removes text that is not running English prose, such as lists of keywords, tables and code.
