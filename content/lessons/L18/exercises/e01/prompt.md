# Where the memory goes

1. `model_state_bytes(n_params, zero=0, dp=1)`: bytes on one GPU for mixed-precision Adam (2 bytes of 16-bit weights, 2 of 16-bit gradients, 12 of fp32 master weights, momentum and variance per parameter), with ZeRO stage $k$ sharding the first $k$ of (optimizer states, gradients, weights) over `dp` ranks. Return a dictionary with keys `weights`, `grads`, `optim`.
2. `activation_bytes(seq, batch, d, heads, layers, tp=1, flash=False, checkpoint=False)`: activations stored for backward, $s\,b\,d\,(34 + 5 a s / d)$ bytes per layer (Korthikanti et al., 2022), divided by `tp`; FlashAttention removes the $5as/d$ term; with full checkpointing, keep only each layer's $2sbd$-byte input plus one layer's activations being recomputed.

## Hints

1. Stage 1 divides only the optimizer states by `dp`, stage 2 also the gradients, stage 3 also the weights.
2. The $5as/d$ term is the $a$ attention matrices of size $s \times s$ (scores, softmax output and dropout mask), which grow with the square of the sequence length.
3. Checkpointing trades memory for one extra forward pass in the backward.
