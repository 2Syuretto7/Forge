# Throughput against latency

In memory-bound decoding each step reads the weights and every sequence's cache: step time $(W + b\,c)/\text{BW}$ for batch $b$, weight bytes $W$ and cache bytes $c$ per sequence.

1. `throughput(batch, weight_bytes, kv_bytes_per_seq, bandwidth)`: tokens per second.
2. `marginal_throughput(...)`: its derivative with respect to the batch, the value of admitting one more sequence.
3. `largest_batch_within(latency_s, ...)`: the largest batch whose step time meets a per-token latency target.

## Hints

1. Throughput $b\,\text{BW}/(W + b c)$ rises with the batch and saturates at $\text{BW}/c$.
2. Its derivative is $\text{BW}\,W/(W + b c)^2$.
3. Serving is a trade: larger batches raise throughput and every user's latency.
