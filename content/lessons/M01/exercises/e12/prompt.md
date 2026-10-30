# How much memory a model needs

- `weight_bytes(n_params, bytes_per_param=2)` returns the bytes needed to store the weights (2 bytes per number in 16-bit formats).
- `adam_bytes(n_params)` returns the bytes needed to train with Adam in mixed precision: 16 bytes per parameter (16-bit weights and gradients, 2 bytes each, plus a 32-bit master copy of the weights and two 32-bit optimizer statistics, 4 bytes each).
- `to_gib(n_bytes)` converts bytes to GiB ($2^{30}$ bytes), the unit GPU tools report.
- `max_params(gib, bytes_per_param)` returns the largest whole number of parameters that fits in `gib` GiB at `bytes_per_param` each.

## Hints

1. Add the per-parameter bytes: 2 + 2 + 4 + 4 + 4.
2. `n_bytes / 2 ** 30`.
3. `int(...)` rounds a positive number down to a whole number; `//` divides and rounds down.
