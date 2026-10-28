# Memory per parameter

1. `bytes_per_param(optimizer="adam", mixed=True)`: training memory per parameter without activations. Mixed precision: fp16 weights and gradients (2 + 2), an fp32 master copy (4), and for Adam two fp32 moments (4 + 4). Plain fp32: weights and gradients (4 + 4), and for Adam two moments (4 + 4). `optimizer` is `"adam"` or `"sgd"` (no state).
2. `training_memory_gb(n_params, optimizer="adam", mixed=True)` and `inference_memory_gb(n_params, bytes_per_weight=2)`.

Notice what mixed precision does not save.

## Hints

1. Write each total as a sum of its parts.
2. Mixed-precision Adam totals 16 bytes, and so does fp32 Adam.
3. The savings of mixed precision are in activations (half the bytes) and speed.
