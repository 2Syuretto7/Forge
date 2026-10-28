# Break it: a cache index bug

`generate_cached_buggy` gives each new token the position of the token before it. Nothing crashes and the text looks plausible; only a comparison with full recomputation reveals it.

Implement `first_divergence(prompt, n, generator)`: run `generator`, then for each new token check whether recomputing the logits from scratch on the sequence before it (with `logits_full`) picks the same token. Return the index of the first new token that disagrees, or `None`.

## Hints

1. Compare against recomputation on the generator's own prefix, so one early mistake is not blamed on every later token.
2. A correct cached generator returns `None`.
3. Run this check on every change to an inference engine; it catches position, mask and cache-length errors.
