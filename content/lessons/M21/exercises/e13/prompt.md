# Evidence counted twice

If a document's words are duplicated (every count doubled), naive Bayes doubles every word's contribution to the log-odds, as if it had seen twice the evidence.

- `doubled_log_odds(model, x)`: the log-odds of `2 * x` (the provided `log_odds`).
- `prior_free_part(model, x)`: the log-odds minus the prior log-ratio, the part that comes from the words.
- `confidence_after_duplication(model, x)`: `(p_before, p_after)`, the probability of class 1 for `x` and for `2 * x`.

A model whose features are copies of each other is overconfident by exactly this mechanism, and real phrases are partial copies.

## Hints

1. The word part is linear in the counts, so it doubles exactly.
2. The prior part does not change.
3. Sigmoid of the log-odds for each.
