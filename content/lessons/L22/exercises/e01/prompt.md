# Prefill and decode on the roofline

Serving has two phases. **Prefill** processes the whole prompt at once: every weight read from memory is used for every prompt token. **Decode** generates one token per sequence per step: every weight is read again for just `batch` tokens.

1. `decode_intensity(n_params, batch, kv_bytes, weight_bytes=2)`: FLOPs per byte of a decode step, $2 N b$ FLOPs over $N \cdot \text{weight\_bytes} + \text{kv\_bytes}$.
2. `prefill_intensity(n_params, prompt_tokens, weight_bytes=2)`: $2 N T$ FLOPs over $N \cdot \text{weight\_bytes}$.
3. `step_time(flops, bytes_moved, peak_flops, bandwidth)`: the roofline time, the larger of the two.

## Hints

1. With 16-bit weights and no cache, decode's intensity is just the batch size.
2. A T4's ridge point is about 200 FLOP/byte in fp16 (L11): decode stays memory-bound up to batches of hundreds.
3. Prefill of a long prompt is compute-bound; decode is memory-bound. Serving systems schedule them differently for that reason.
