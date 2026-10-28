# From a pair to a training example

Implement `build_example(prompt, response, bos, sep, eos, pad, max_len)`. The token sequence is `[bos] + prompt + [sep] + response + [eos]`, truncated to `max_len + 1` tokens and padded with `pad`. Return `(inputs, targets, mask)`, each of length `max_len`: the inputs are the first `max_len` ids, the targets the same ids shifted left by one, and the mask is 1 exactly where the target is a response token or the `eos`.

## Hints

1. Track each id's kind (prompt or response) alongside the ids, and shift the kinds with the targets.
2. The separator belongs to the prompt: the model is never trained to produce it.
3. The `eos` is part of the response: a model that never learns to stop keeps generating.
