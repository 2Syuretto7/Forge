# Break it: training on the prompt

Leave the mask out and the model is also trained to produce the prompts, and with long prompts most of its gradient goes there. A unigram model shows the cost in one line: fit next-token frequencies on everything, and the response distribution gets diluted by the prompt's.

1. `fit_unigram(tokens, mask, vocab)`: token frequencies over the positions where `mask` is 1, with add-one smoothing.
2. `response_ce(p, tokens, mask)`: the mean $-\ln p(t)$ over the masked-in tokens.

## Hints

1. `np.bincount(..., minlength=vocab)` counts tokens.
2. Fitting with the response mask estimates the response distribution; fitting with all ones estimates a mixture of prompts and responses.
3. The longer the prompts, the worse the unmasked fit is on responses.
