# Break it: overflowing scores and the range-precision trade

## Attention logits in fp16

Dot products of long vectors grow with their length and with the magnitude of their entries. In an fp16 matrix product without scaling, scores can exceed 65504 and become infinite, and an infinity in a softmax produces NaN everywhere it touches.

:::exercise{ref=e11}
:::

## bf16 or fp16?

::::predict{id=p5 kind=choice answer=c}
You must store both activations as large as $10^5$ and the difference between $1.000$ and $1.001$. Which 16-bit format keeps both?

- fp16.
- bf16.
- Neither: fp16 overflows at $10^5$ and bf16 cannot tell 1.000 from 1.001.
- Both.

:::reveal
fp16's largest value is 65504, so $10^5$ overflows; bf16's spacing near 1 is about 0.0078, so 1.001 rounds to 1.000. Each 16-bit format gives up one of the two, which is why training recipes keep reductions and master weights in fp32, and why fp8 needs per-tensor scale factors.
:::
::::

:::exercise{ref=e12}
:::

## What to take away

- Use bf16 where the hardware supports it (no loss scaling needed); use fp16 with a dynamic loss scaler otherwise.
- Keep master weights, optimizer state and reductions in fp32.
- When a half-precision run produces NaN, look for an overflow first: large logits, an unscaled product, a loss scale that is too high.
