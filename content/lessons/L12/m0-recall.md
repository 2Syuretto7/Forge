# Recall bridge: rooflines, layer norm and attention

From L11: a kernel is limited by the slower of its FLOPs and its bytes, and tiling and fusion cut the bytes. From L10: layer norm normalizes each row with its own mean and variance. From L13: attention computes $\operatorname{softmax}(QK^\top/\sqrt d)\,V$, and its $N \times N$ score matrix is the expensive part. This lesson writes those operations as GPU kernels. Reviews due from those lessons appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
Unfused, a row softmax reads and writes its data several times; a fused one reads it [[1]] time and writes it once.
:::
:::step
The scores of one attention head over $N = 1024$ positions form a matrix with [[1048576]] entries.
:::
:::step
The softmax of $(0, \ln 3)$ is $(0.25, 0.75)$. Shifting both scores by 100 gives the weight [[0.75]] to the second entry.
:::
::::
