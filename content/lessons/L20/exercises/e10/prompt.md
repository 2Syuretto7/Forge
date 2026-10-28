# What the teacher knows

A teacher's probabilities for the wrong answers carry information ("this 2 looks a little like a 7"). A temperature above 1 exposes it.

1. `soften(logits, T)`: $\operatorname{softmax}(z/T)$.
2. `entropy(p)` in nats.
3. `topk_teacher(p, k)`: keep the $k$ largest probabilities and renormalize, the usual way to store a teacher's outputs for a whole corpus.

## Hints

1. Raising $T$ flattens the distribution but never changes the order of the classes.
2. Storing full distributions costs one number per vocabulary entry per token; the top 8 or so usually carry almost all the mass.
3. Renormalize after truncating, so the stored teacher is still a distribution.
