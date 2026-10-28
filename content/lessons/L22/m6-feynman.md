# Explain it plainly: serving a language model

Explain to a backend engineer why serving a language model is limited by memory, and the main techniques that make it fast.

- Write 150 to 400 words.
- Explain prefill versus decode and why decode is memory-bound.
- Explain the KV cache and batching, including continuous batching.
- Explain weight quantization and speculative decoding, and why the latter does not change the output distribution.

:::feynman{id=f1 prompt="Explain why serving a language model is limited by memory bandwidth and how the KV cache, continuous batching, weight quantization and speculative decoding make it faster, including why speculative decoding preserves the output distribution." key_points="Decoding one token reads every weight once while doing about two operations per weight, so it is limited by memory bandwidth, unlike prefill|The KV cache stores each earlier token's keys and values so each step only processes the new token, and its size limits the batch|Batching shares each weight read among many sequences, and continuous batching admits and retires sequences at every step|Weight-only quantization stores weights in 8 or 4 bits with scales, cutting the bytes read and so the step time|Speculative decoding lets a small draft propose tokens that the large model verifies in one pass, accepting with probability min(1, p/q) and resampling from the residual, which leaves the distribution exactly the large model's"}
:::
