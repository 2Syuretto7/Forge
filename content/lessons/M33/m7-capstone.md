# Capstone: fast, accurate and accounted for

Approximate a $2000 \times 400$ matrix at rank 10 to within 1 percent of the optimal error, at more than five times the speed of the full SVD, and account for the cost: list every matrix product in your method with its flops and bytes, and place each on the roofline of a laptop-class machine.

:::exercise{ref=capstone}
:::

## When you finish

You can tell whether a computation is limited by memory or by arithmetic, solve systems with only matrix-vector products, and compress a matrix at a fraction of the cost of its SVD. L07 places real GPU kernels on the roofline; M34 proves why random projections preserve geometry; M38 uses low-rank structure in efficient models.

:::edge{to=L07 text="GPU kernels on the roofline."}
:::

:::edge{to=M34 text="random projections and high-dimensional geometry."}
:::
