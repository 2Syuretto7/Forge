# Break it: a saturated softmax and a mask that leaks

## Forgetting the scale

:::exercise{ref=e11}
:::

## An off-by-one mask

The most dangerous transformer bug produces a model that looks excellent in training. If the causal mask lets position $i$ see position $i + 1$, the model can read the token it is supposed to predict; the training loss falls far below anything achievable, and generation, where the next token does not exist yet, produces garbage.

::::predict{id=p5 kind=choice answer=d}
How can you detect a leaking mask without training anything?

- Check that every row of attention weights sums to 1.
- Check the loss after one step.
- Count the masked entries.
- Change the input at one position and check that no output at an earlier position changes.

:::reveal
Causality is a statement about dependence: the output at position $t$ must not depend on inputs after $t$. Perturbing one position and checking earlier outputs tests exactly that, for any implementation, without trusting how the mask was built. Row sums and counts can look right with the diagonal in the wrong place.
:::
::::

:::exercise{ref=e12}
:::

## What to take away

- Always scale scores by $1/\sqrt{d_k}$; watch for weights near one-hot early in training.
- Test causality by perturbation, not by inspecting the mask.
- When a model's training loss is suspiciously good, look for a leak before celebrating.
