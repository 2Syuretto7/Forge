# Recall bridge: the SVD, the transformer and a pretrained model

From M14: the SVD writes any matrix as a sum of rank-one pieces ordered by size, and keeping the largest $r$ gives the best rank-$r$ approximation. From L09: a transformer block is a handful of weight matrices around attention. From L15: pretraining leaves you with a model that continues text well and follows no instructions at all. This lesson adapts that model to a task cheaply and without wrecking what it already knows. Reviews due from M14, L09 and L15 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
A matrix with singular values $3, 1, 0.5$ loses, at rank 1, a relative Frobenius error of $\sqrt{(1 + 0.25)/(9 + 1 + 0.25)} \approx$ [[0.349|tol=0.001]].
:::
:::step
A $4096 \times 4096$ weight matrix has [[16777216]] entries.
:::
:::step
Two factors of rank 8 replacing an update of it, $8 \times 4096$ and $4096 \times 8$, have [[65536]] entries between them.
:::
::::
