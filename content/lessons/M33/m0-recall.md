# Recall bridge: from exact answers to fast ones

M14 built the SVD and proved that truncating it gives the best low-rank approximation; M26 measured how floating point loses digits and how conditioning decides how many. Both treated the computation as free. This lesson counts its cost, in arithmetic and in data moved, and finds algorithms that reach the same answers at a fraction of the cost: by blocking, by iterating, and by randomizing. Clear your due cards above first.

:::edge{from=M14 text="the SVD, Eckart-Young and low-rank approximation"}
:::

:::edge{from=M26 text="floating point, conditioning and stable algorithms"}
:::

## What carries over

The SVD and its truncation (M14); the QR factorization and orthonormal bases (M12); eigenvalues of symmetric matrices and the condition number (M13, M26); and machine epsilon with the rule that a backward-stable method loses about $\log_{10}\kappa$ digits (M26).
