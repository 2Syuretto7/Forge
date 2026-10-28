# A gradient checker for the engine

Implement `gradcheck(fn, inputs, eps=1e-6)`. `fn` maps a list of Tensors to a scalar Tensor. Run `fn` once and call `backward()` (after clearing the inputs' gradients) to get the engine's gradients; then estimate each input's gradient by central differences, perturbing one entry of `t.data` at a time and calling `fn` again. Return one relative error per input:

$$
\frac{\lVert g_{\text{engine}} - g_{\text{numeric}} \rVert}{\max(\lVert g_{\text{engine}} \rVert + \lVert g_{\text{numeric}} \rVert,\ 10^{-12})}.
$$

Then use it. `buggy_bias_add` in the starter has the broadcasting bug from Movement 5. The tests check that your checker passes the engine's correct operations and flags the buggy one, on the bias only.

## Hints

1. Restore every perturbed entry before moving on to the next.
2. An input that receives no gradient has an engine gradient of zeros.
3. Use a random weighting `(f(...) * G).sum()` as the scalar, so errors in different output entries cannot cancel.
