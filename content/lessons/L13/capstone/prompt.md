# Capstone: train a transformer on Shakespeare

Open the Colab notebook with a **T4 GPU** runtime and work through it:

1. Write the forward pass of `CausalSelfAttention` (one fused query-key-value projection, scaled scores, causal mask, softmax, weighted values, merged heads, output projection) without calling PyTorch's fused attention; the tests compare your result with it.
2. Write `Block.forward` (pre-norm, two residual branches) and `GPT.forward` (token plus position embeddings, blocks, final layer norm, output layer), and `param_formula`, the parameter count in closed form.
3. Train with the provided loop and the reference settings (or your own) to a validation loss below **1.70 nats per character**, and sample some text.

The autograder checks your attention against PyTorch's, causality by perturbation, the parameter formula, that training reduces the loss, the validation target and the sampler.
