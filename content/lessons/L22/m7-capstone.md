# Capstone: an inference server that meets its targets

The notebook trains a small byte-level GPT (6 layers, width 384, about 10.7 million parameters) for a few minutes on a T4, so there is a model to serve. You write the engine: `prefill` and `decode_step` over a key-value cache with one slot per sequence, each slot at its own position; a continuous-batching `serve` loop that admits requests as they arrive and retires them as they finish; and weight-only int8 quantization with a scale per row. Then a workload of 64 requests arriving at 40 per second is replayed against your server to measure latency, and the same requests, all queued at once, measure throughput against serving one request at a time.

The targets: at least **4 times** the throughput of one-at-a-time serving with every request queued, and on the arriving workload a 95th-percentile gap between consecutive tokens under **50 ms** and a 95th-percentile time to first token under **500 ms**. A T4 meets them with room to spare; so does a CPU runtime, narrowly. The autograder also checks that cached and batched generation match full recomputation token for token, that int8 storage cuts the linear weights to about a quarter of float32 while the validation loss moves by less than 0.02, and the report.

:::exercise{ref=capstone}
:::

:::colab{notebook=L22}
:::

## When you finish

You have built the core of a serving engine. Production engines add paged memory, fused kernels for attention and dequantization, and speculative decoding; L24 serves the model you train end to end.

:::edge{to=L24 text="Serving the final model."}
:::
