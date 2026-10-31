# Residual branches without normalization

The unnormalized residual stack (`res`) explodes at initialization. Fix it without any normalization:

1. `branch_scale_for(depth)` returns $1/\sqrt{\text{depth}}$, the factor that keeps $(1 + \alpha^2)^{\text{depth}}$ bounded.
2. `compare_branch_scaling(depth=20, width=32, steps=300, lr=3e-3, seed=0)` trains `res` with branch scale 1 and with `branch_scale_for(depth)` (your `train` is provided) and returns `{"unscaled": loss, "scaled": loss}`, each the mean of the last 30 minibatch losses.

Scaling or zero-initializing the last layer of each branch is how very deep networks are trained without (or alongside) normalization.

## Hints

1. Pass the scale through `train(..., branch_scale=s)`; `init_stack` multiplies every `W{l}` by it.
2. Use the same seed for both runs so only the scale differs.
3. Compare the first few losses of the two runs as well: the unscaled one starts in the tens of thousands.
