# Capstone: a numerically hardened library

Write the dozen functions every training loop calls (log-sum-exp, softmax and log-softmax, sigmoid, softplus and log-sigmoid, cross-entropy and binary cross-entropy from logits, a mean and variance, $\log(1 - e^{-a})$ and a compensated sum) so that they return accurate, finite answers on an adversarial suite of 40 extreme inputs, written as if NumPy raised an error on any overflow or invalid operation.

:::exercise{ref=capstone}
:::

## When you finish

You can predict where a computation loses digits and rewrite it so it does not. M33 applies the same thinking to factorizations of large matrices; L13 trains in bf16 and fp8, where every lesson of this one is pushed to its limit.

:::edge{to=L13 text="mixed precision: bf16, fp8 and float32 accumulators."}
:::
