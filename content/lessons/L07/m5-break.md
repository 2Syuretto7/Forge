# Break it: symmetry, dead units and explosions

Section 7 named three ways a network can fail before learning anything. Each exercise here builds one on purpose and measures it.

## Symmetry

:::exercise{ref=e10}
:::

## Dead ReLUs

:::exercise{ref=e11}
:::

::::predict{id=p5 kind=choice answer=a}
After one step with a learning rate 100 times too large, 70 percent of a layer's ReLU units output zero on every training example. Lowering the learning rate back to normal, what happens to those units?

- They stay dead: their gradients are exactly zero, so nothing moves their weights again.
- They recover slowly as the other units' gradients pull them back.
- They recover immediately once the learning rate is reasonable.
- They become negative and start contributing with the opposite sign.

:::reveal
A dead ReLU has zero output and zero local derivative on every input, so the gradient with respect to its incoming weights and bias is exactly zero. No learning rate fixes that. Remedies are prevention: sensible initialization, learning-rate warmup (L09), or activations with a nonzero slope for negative inputs.
:::
::::

## Exploding activations

:::exercise{ref=e12}
:::

:::widget{name=ActivationStats depth=10 init=unit act=relu}
:::

## What to take away

- Initialize weights randomly with a scale near $\sqrt{2/n_{\text{in}}}$ for ReLU and $\sqrt{1/n_{\text{in}}}$ for tanh; start biases at zero.
- Watch the fraction of active ReLU units and the scale of activations per layer during the first steps of training.
- A network that does not learn at all is usually broken by one of these three, not by a subtle optimization problem.
