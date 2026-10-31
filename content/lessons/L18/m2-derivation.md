# Derivation: where the time and memory go

## 1. Prefill and decode

Serving a request has two phases. **Prefill** runs the prompt's $T$ tokens through the model in one pass: each weight read from memory serves $T$ tokens, an arithmetic intensity of about $T$ FLOPs per byte in 16-bit, so long prompts are compute-bound. **Decode** then generates one token per step per sequence: each weight read serves only the $b$ sequences in the batch, an intensity of about $b$. Below the ridge point (about 150 on an A100, 200 on a T4) decode is memory-bound, and a step takes the time to read the weights and the caches:
$$
t_\text{step} \approx \frac{\text{weight bytes} + \text{cache bytes}}{\text{bandwidth}}.
$$
The two phases are measured separately: **time to first token** (mostly prefill) and **inter-token latency** (decode).

::::derivation{id=d1 title="Decode on the roofline"}
:::step
At batch 1 with 16-bit weights, decode's intensity is about [[1]] FLOP per byte.
:::
:::step
To reach an A100's ridge point of 312 TFLOP/s over 2.04 TB/s, a batch of about [[153|tol=1]] sequences would be needed (ignoring the caches).
:::
::::

:::edge{from=L08 text="kernels bound by bytes, and FlashAttention"}
:::

:::widget{name=Roofline hardware=a100 precision=fp16}
:::

## 2. The KV cache

At every decode step, attention needs the keys and values of all earlier tokens. Recomputing them would cost a full forward pass over the prefix per token; instead they are **cached**: per token, a key and a value for every layer and every key-value head,
$$
\text{bytes per token} = 2 \times n_\text{layers} \times n_\text{kv heads} \times d_\text{head} \times \text{bytes per number}.
$$
Each step then computes only the new token's query, key and value and attends over the cache. The cache grows with batch and context and becomes the main consumer of memory. **Grouped-query attention** (GQA) shares each key-value head among a group of query heads and divides the cache by the group size; multi-query attention uses a single key-value head.

::::derivation{id=d2 title="Cache arithmetic"}
:::step
Llama 2 7B (32 layers, 32 key-value heads of dimension 128, 16-bit) stores $2 \cdot 32 \cdot 32 \cdot 128 \cdot 2 =$ [[524288]] bytes per token.
:::
:::step
With 8 key-value heads instead of 32 that becomes [[131072]] bytes.
:::
::::

:::edge{from=L09 text="attention over keys and values"}
:::

## 3. Batching

Batching shares each weight read among sequences, raising throughput until the step becomes compute-bound or the caches fill memory. **Static batching** groups requests and runs each group until its longest member finishes, so short requests wait and new arrivals queue behind the whole batch. **Continuous batching** (Orca, 2022) schedules at every step: finished sequences leave immediately and waiting ones take their slots. **Paged attention** (vLLM, 2023) stores each sequence's cache in fixed-size pages allocated as it grows, so memory is not reserved for tokens that are never generated, more sequences fit, and pages holding a shared prompt can be shared. Throughput and latency trade against each other: a larger batch makes more tokens per second and each token slower.

## 4. Quantization

Decode time is mostly reading weights, so storing them in fewer bits speeds it up almost proportionally. **Weight-only quantization** stores integers and a scale per row (or per group of weights) and dequantizes on the fly: with a scale $s$, each weight's error is at most $s/2$. What matters is the error in the layer's **outputs** on real inputs, so methods like GPTQ round to minimize $\|X W^\top - X \hat W^\top\|$ on calibration data. Large models have a few input features with very large activations: with one scale per tensor they wreck the precision of everything else, and the LLM.int8 method keeps those few features in 16 bits.

::::derivation{id=d3 title="Bytes saved"}
:::step
In int8, the 6.74-billion-parameter model takes about [[6.74|tol=0.01]] GB instead of 13.48: the decode step roughly halves.
:::
::::

:::edge{from=L13 text="fewer bits per number"}
:::

## 5. Speculative decoding

Because decode is memory-bound, checking several tokens costs about as much as generating one: one forward pass of the target model over $\gamma$ proposed tokens reads the weights once. A small **draft** model proposes $\gamma$ tokens; the target scores them all in one pass and accepts each proposed token $x$ with probability $\min(1, p(x)/q(x))$, where $p$ and $q$ are the target's and the draft's probabilities. At the first rejection it samples a replacement from $\max(0, p - q)$, renormalized. The emitted token's distribution is exactly $p$: accepting gives $q(x)\min(1, p(x)/q(x)) = \min(p(x), q(x))$, and the rejected mass $1 - \sum \min(p, q)$, spread as the residual, supplies the remaining $p(x) - \min(p(x), q(x))$ (Leviathan et al., 2023). With each token accepted with probability $\alpha$, a target pass yields on average
$$
\frac{1 - \alpha^{\gamma + 1}}{1 - \alpha}
$$
tokens; a draft that costs a fraction $c$ of the target per token makes the speedup that divided by $\gamma c + 1$.

::::derivation{id=d4 title="Speculative speedup"}
:::step
With $\alpha = 0.8$ and $\gamma = 4$, each target pass yields $(1 - 0.8^5)/0.2 \approx$ [[3.36|tol=0.01]] tokens.
:::
:::step
If the draft costs 5% of the target per token, the speedup is $3.36/(4 \cdot 0.05 + 1) \approx$ [[2.8|tol=0.02]].
:::
::::

:::edge{from=L16 text="a distilled student as the draft model"}
:::

## 6. Measuring

Benchmark the phases separately, with warm-up and synchronization (L07): time to first token as a function of prompt length, inter-token latency as a function of batch and context, and throughput at a stated latency target. Report the distribution of latencies (median and 95th percentile), not just the mean: users wait for the slow requests.

:::edge{to=L20 text="The final capstone serves its own model."}
:::
