# Explain it plainly: how FlashAttention saves memory and time

Explain to an engineer who knows how attention is computed why FlashAttention is faster and uses less memory, although it performs the same arithmetic.

- Write 150 to 400 words.
- Use the picture of the score matrix and the GPU's small, fast on-chip memory.
- Explain the online softmax and why blocks can be processed one at a time.
- Mention what the backward pass stores instead of the full matrix.

:::feynman{id=f1 prompt="Explain why FlashAttention is faster and uses less memory than standard attention although it does the same arithmetic, including the online softmax and what the backward pass keeps." key_points="Standard attention writes the N by N score and probability matrices to device memory and reads them back, which is slow because it is memory-bound|FlashAttention processes keys and values in tiles that fit in fast on-chip memory, so the full matrix is never stored|The online softmax keeps a running maximum and sum and rescales them when the maximum grows, giving the exact softmax in one pass|The backward pass stores only one log-sum-exp per query and recomputes the probabilities tile by tile|Memory falls from quadratic to linear in sequence length and speed improves because far fewer bytes move"}
:::
