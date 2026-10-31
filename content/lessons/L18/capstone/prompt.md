# Capstone: an inference server that meets its targets

Open the Colab notebook with a **T4 GPU** runtime and work through it:

1. Write `prefill` and `decode_step` over a key-value cache with one slot per sequence. The notebook checks that cached generation matches full recomputation.
2. Write `serve`, a continuous-batching loop: admit arrived requests into free slots, run one decode step over every active slot, and free slots as requests finish, recording when each token was produced.
3. Run the workload as it arrives to measure time to first token and inter-token latency, then with every request queued to compare throughput with serving one request at a time.
4. Write `quantize_int8` and `Int8Linear.forward`, and measure the size and quality of the int8 model.
5. Write a report of at least 80 words: the model and workload, throughput and latency against the targets, why batching helps decode, and what int8 did.

The targets: at least **4x** the one-at-a-time throughput with every request queued, and on the arriving workload a 95th-percentile inter-token latency under **50 ms** and a 95th-percentile time to first token under **500 ms**. The autograder also checks that batched decoding of prompts of different lengths matches recomputation, that at least 95% of served requests match it exactly, the int8 rounding error and size, a validation loss change under 0.02, and the report.
