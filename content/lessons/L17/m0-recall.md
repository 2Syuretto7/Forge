# Recall bridge: tensor cores and the roofline

From L11: a T4 multiplies matrices at 8.1 TFLOP/s in fp32 and 65 TFLOP/s in fp16 on its tensor cores, and memory-bound operations run at the speed of bytes. Halving the bytes per number halves their time; switching matrix products to fp16 multiplies their roof by eight. The price is numerical: fewer bits for the exponent and the mantissa. Reviews due from L11 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
The T4's fp16 tensor-core peak is $65/8.1 \approx$ [[8.02|tol=0.02]] times its fp32 peak.
:::
:::step
A memory-bound kernel that moves 4 bytes per value in fp32 moves [[2]] in fp16.
:::
::::
