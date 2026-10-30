# Capstone: a rotary position-encoding toy

Large language models need to know where each token is. The rotary encoding (RoPE) turns pairs of coordinates of each query and key vector by angles proportional to the token's position, at several speeds. Your capstone builds it, proves the property that makes it work, and checks the property on a thousand random pairs.

:::exercise{ref=capstone}
:::

## When you finish

You have used rotation, complex numbers and Euler's formula on the exact mechanism inside many current language models. M09 makes vectors and dot products general, M10 makes rotations into matrices, and in L13 the rotary encoding sits inside a full attention layer.

:::edge{to=L13 text="the rotary encoding inside an attention layer."}
:::
