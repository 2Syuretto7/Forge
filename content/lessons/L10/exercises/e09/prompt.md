# Temperature and entropy

1. `tempered_xent(logits, y, T)`: the mean cross-entropy of $\operatorname{softmax}(z/T)$ against labels `y`, and its gradient with respect to the logits $z$.
2. `entropy_at(logits, T)`: the entropy in nats of $\operatorname{softmax}(z/T)$ for one vector of logits.

Temperature divides the logits, so by the chain rule it divides the gradient too. The same tempered softmax appears in distillation, where a teacher's soft predictions at high temperature train a student.

## Hints

1. $\partial L/\partial z = (\operatorname{softmax}(z/T) - \text{onehot}(y)) / (nT)$.
2. Guard the logarithm of zero probabilities when computing the entropy.
3. The entropy increases with $T$, from 0 (greedy) toward $\ln V$ (uniform).
