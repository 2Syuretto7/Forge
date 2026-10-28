# Recall bridge: initialization, Adam and warmup

From L09: variance-preserving initialization keeps activations at unit scale at the start of training, Adam takes steps of roughly the learning rate per weight whatever the gradient's size, and warmup keeps the first steps small. This lesson asks what keeps a deep network trainable after the first step, when initialization no longer controls the scale. Reviews due from L09 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
He initialization for a ReLU layer with $n_{\text{in}} = 512$ uses standard deviation $\sqrt{2/512} =$ [[0.0625]].
:::
:::step
A linear warmup from 0 to a peak of $10^{-3}$ over 1000 steps gives, at step 250, a rate of [[0.00025]].
:::
:::step
With variance $1/n_{\text{in}}$ instead of $2/n_{\text{in}}$, a ReLU layer halves the second moment of the activations. After 10 such layers it has shrunk by $2^{-10} \approx$ [[0.0009766|tol=0.000001]].
:::
::::

By the end of this lesson you will have built batch norm, layer norm and RMSNorm with their backward passes, a 30-layer network in five variants, and the measurements that tell them apart.
