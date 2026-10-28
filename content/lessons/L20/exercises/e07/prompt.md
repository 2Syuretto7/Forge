# Distillation

A small student learns from a large teacher's whole distribution, not just the right answer. Hinton et al. soften both with a temperature $T$ and mix the result with the ordinary loss:
$$
\mathcal{L} = \alpha\, T^2\, \mathrm{KL}\bigl(\operatorname{softmax}(t/T) \,\|\, \operatorname{softmax}(s/T)\bigr) + (1 - \alpha)\, \mathrm{CE}(s, y).
$$

Implement `distill_loss(student, teacher, labels, T, alpha)`, averaged over rows, with its gradient with respect to the student logits. `softmax(z, T)` is provided.

## Hints

1. The gradient of the KL term with respect to $s$ is $(p_s - p_t)/T$; the factor $T^2$ makes it $T(p_s - p_t)$.
2. The $T^2$ keeps the two terms on comparable scales as $T$ changes.
3. The cross-entropy term uses the unsoftened student, $T = 1$.
