# Explain it plainly: why training in half precision works

Explain to an engineer who knows that fp16 has only about three significant digits why neural networks can be trained in it without losing accuracy.

- Write 150 to 400 words.
- Use the example of a small weight update being added to a weight.
- Explain master weights, fp32 accumulation and loss scaling.
- Mention the difference between fp16 and bf16.

:::feynman{id=f1 prompt="Explain why neural networks can be trained in 16-bit floating point without losing accuracy, covering master weights, fp32 accumulation, loss scaling and the difference between fp16 and bf16." key_points="Half precision has few mantissa bits, so a small update added to a much larger weight can round away entirely|An fp32 master copy of the weights accumulates the updates, while forward and backward passes use half-precision copies|Matrix products accumulate in fp32 and reductions such as softmax and normalization stay in fp32|fp16's narrow range makes small gradients underflow, so the loss is scaled up before the backward pass and the gradients scaled back down|bf16 keeps fp32's exponent range so it needs no loss scaling, at the cost of less precision"}
:::
