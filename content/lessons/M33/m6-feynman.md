# Explain it plainly: the data, not the arithmetic

Explain why moving data, not arithmetic, is usually the bottleneck.

Guidelines:

- Write 150 to 400 words.
- Use the matrix-vector product and the matrix-matrix product as the two examples.
- Give rough numbers for a real chip.
- Say what algorithms do about it.

:::feynman{id=f1 prompt="Explain why moving data, not arithmetic, is usually the bottleneck." key_points="A chip can do far more arithmetic per second than it can move bytes from memory per second; the ratio, the ridge point, is tens of flops per byte|A kernel's arithmetic intensity, flops per byte moved, decides which limit applies: below the ridge it waits on memory|A matrix-vector product does about two flops per matrix entry read, half a flop per byte in fp32, so it runs at memory speed|A large matrix product does order n flops per number, but only if each number is reused many times while it is in fast memory, which blocking arranges|Algorithms that batch work into matrix products, like blocked factorizations and the randomized SVD, run near peak, while those built on matrix-vector steps do not"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that if A is symmetric positive definite and the search directions p_0, ..., p_{n-1} are nonzero and A-conjugate, then exact line minimization of f(x) = x^T A x / 2 - b^T x along each direction in turn reaches the solution of Ax = b in at most n steps." key_points="Shows that A-conjugate nonzero directions are linearly independent, so n of them span R^n|Writes the error x* - x_0 as a combination of the directions, with coefficients found by multiplying by p_j^T A|Shows that exact line minimization along p_k gives the step alpha_k = p_k^T r_k / (p_k^T A p_k)|Shows that this step equals the coefficient of p_k in the expansion of the error, because the earlier steps do not change p_k^T A times the error|Concludes that after n steps every coefficient has been removed and x_n = x*"}
:::
