# Derivation: floating-point formats and mixed-precision training

## 1. IEEE formats

A binary floating-point number with $e$ exponent bits and $m$ mantissa bits stores a sign $s$, a biased exponent $E$ and a fraction $f$:
$$
x = (-1)^s \cdot \left(1 + \frac{f}{2^m}\right) \cdot 2^{E - \text{bias}}, \qquad \text{bias} = 2^{e-1} - 1,
$$
for $E$ from 1 to $2^e - 2$. $E = 0$ encodes **subnormals**, $(f/2^m) \cdot 2^{1 - \text{bias}}$, which fill the gap down to zero; $E = 2^e - 1$ encodes infinities and NaN. The mantissa sets the precision, the **machine epsilon** $2^{-m}$ (the gap after 1); the exponent sets the range.

| Format | Exponent, mantissa bits | Largest | Smallest normal | Epsilon |
| --- | --- | --- | --- | --- |
| fp32 | 8, 23 | $3.4 \times 10^{38}$ | $1.2 \times 10^{-38}$ | $1.2 \times 10^{-7}$ |
| bf16 | 8, 7 | $3.4 \times 10^{38}$ | $1.2 \times 10^{-38}$ | $7.8 \times 10^{-3}$ |
| fp16 | 5, 10 | 65504 | $6.1 \times 10^{-5}$ | $9.8 \times 10^{-4}$ |
| fp8 E4M3 | 4, 3 | 448 | $1.6 \times 10^{-2}$ | 0.125 |
| fp8 E5M2 | 5, 2 | 57344 | $6.1 \times 10^{-5}$ | 0.25 |

::::derivation{id=d1 title="The fp16 range"}
:::step
fp16 has bias $2^4 - 1 = 15$. The largest exponent field for finite numbers is 30, so the largest value is $(2 - 2^{-10}) \cdot 2^{15} =$ [[65504]].
:::
:::step
The smallest normal number is $2^{1 - 15} = 2^{-14} \approx$ [[0.000061|tol=0.000001]], and the smallest subnormal $2^{-24} \approx 6 \times 10^{-8}$.
:::
::::

## 2. Rounding and spacing

Results are rounded to the nearest representable value, with ties going to the one with an even last bit. Around $x$ the representable numbers are $\text{ulp}(x) = 2^{\lfloor \log_2 |x| \rfloor - m}$ apart, so the relative error of a rounding is at most $2^{-m-1}$.

::::derivation{id=d2 title="Spacing"}
:::step
In fp16, the spacing between 2048 and the next number is $2^{11 - 10} =$ [[2]], so $2048 + 1$ rounds back to 2048.
:::
:::step
In bf16, the spacing just above 1 is $2^{-7} \approx$ [[0.0078|tol=0.0001]]: an update of 0.001 to a weight of 1 rounds away.
:::
::::

## 3. Accumulation

Adding many small numbers into a large running sum fails once the sum's spacing exceeds twice the addend: each addition rounds back to the old sum. Summing $10^4$ copies of 0.01 in fp16, the sum stops growing at 32, where the spacing is $2^{-5} = 0.03125$. Remedies: accumulate in fp32 (what tensor cores do inside a matrix product), sum pairwise, or carry the rounding error forward (Kahan summation).

## 4. Mixed-precision training

The standard recipe (Micikevicius et al., 2018):

- keep **fp32 master weights**; cast a half-precision copy for the forward and backward passes;
- run matrix products in half precision with fp32 accumulation; keep reductions (softmax, normalization, the loss) in fp32. PyTorch's `autocast` applies these per-operation rules;
- with fp16, use **loss scaling**: multiply the loss by $S$ before the backward pass, so that gradients smaller than fp16's subnormal range survive, then divide the gradients by $S$ before the update. **Dynamic** scaling starts large, halves $S$ and skips the step when any gradient is infinite or NaN, and doubles it after a run of good steps;
- with bf16, which has fp32's range, loss scaling is unnecessary, but its 7-bit mantissa makes master weights essential.

::::derivation{id=d3 title="Loss scaling"}
:::step
A gradient of $10^{-8}$ underflows to 0 in fp16. Scaled by $S = 2^{16} = 65536$, it becomes about [[0.000655|tol=0.000005]], comfortably representable.
:::
:::step
After [[2000]] consecutive good steps, PyTorch's default `GradScaler` doubles the scale.
:::
::::

**Memory.** Mixed precision with Adam stores fp16 weights and gradients (2 + 2 bytes per parameter) plus fp32 master weights and two moments (12 bytes): 16 bytes per parameter, the same as fp32 Adam. The savings are in activations, which are stored in half precision, and in time.

## 5. Stochastic rounding

Round $x$, between grid points $\ell$ and $\ell + \delta$, up with probability $(x - \ell)/\delta$ and down otherwise. The expected result is exactly $x$, so repeated tiny updates accumulate on average instead of vanishing. Some low-precision training methods use it in place of master weights.

## 6. fp8

Two 8-bit formats are used in training on recent GPUs: **E4M3** (more precision, range up to 448) for weights and activations, **E5M2** (more range, up to 57344) for gradients. With so little range, each tensor carries its own **scale factor**, chosen from the largest magnitude seen recently, so that its values fill the representable range.

:::edge{from=L11 text="tensor cores and the roofline"}
:::

:::edge{to=L14 text="Train the GPT in reduced precision."}
:::

:::edge{to=L18 text="Sixteen bytes per parameter is the budget distributed training splits across GPUs."}
:::

:::edge{to=L22 text="Low-precision weights and caches at inference."}
:::
