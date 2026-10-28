# Explain it plainly: why deep networks need residuals and normalization

Explain to a programmer who has trained a three-layer network why simply stacking 30 layers fails, and what residual connections and normalization layers each do about it.

- Write 150 to 400 words.
- Use a concrete picture, such as a message passed along a line of 30 people.
- Explain what goes wrong in the forward pass and in the backward pass.
- Mention one trade-off or failure of the fixes.

:::feynman{id=f1 prompt="Explain why a plain 30-layer network trains badly, and what residual connections and normalization layers each contribute to making it trainable." key_points="In a plain deep stack the signal and the gradient are multiplied by many layer Jacobians, so they shrink or grow geometrically with depth|A residual connection adds the input back, so the backward pass always has an identity path that carries the gradient unchanged|Normalization rescales activations to a fixed scale during training, not only at initialization|Pre-norm keeps the skip path clean while post-norm normalizes it at every layer and needs warmup|A concrete trade-off such as batch norm depending on the batch, or the residual stream growing without normalization"}
:::
