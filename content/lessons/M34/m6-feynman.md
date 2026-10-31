# Explain it plainly: perpendicular by default

Explain why almost all random directions in high dimension are perpendicular.

Guidelines:

- Write 150 to 400 words.
- Start from the dot product as a sum of products of coordinates.
- Give the typical angle in 4,096 dimensions.
- Say when the statement fails.

:::feynman{id=f1 prompt="Explain why almost all random directions in high dimension are perpendicular." key_points="The dot product of two random vectors is a sum of d independent terms with mean zero, so it grows only like the square root of d|Each vector's length also concentrates near the square root of d, so the cosine is about 1 over the square root of d|In 4,096 dimensions the angle is 90 degrees give or take about 0.9 degrees, and large deviations are exponentially unlikely|High-dimensional space therefore holds far more nearly orthogonal directions than its dimension|The argument needs independent, centered coordinates; vectors sharing a common component are not nearly perpendicular until it is removed"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove the Johnson-Lindenstrauss lemma: for n points and a d x k matrix R with independent N(0, 1/k) entries, every squared pairwise distance is preserved within a factor 1 +- eps with positive probability when k >= 4 ln n / (eps^2/2 - eps^3/3)." key_points="Fixes one difference vector x and shows that k |R^T x|^2 / |x|^2 is a chi-square variable with k degrees of freedom|Applies Markov's inequality to exp(t Z) and uses the chi-square moment generating function (1 - 2t)^(-k/2)|Optimizes t to obtain the bound ((1 + eps) e^(-eps))^(k/2) and simplifies it with log(1 + eps) <= eps - eps^2/2 + eps^3/3|Bounds the lower tail similarly, so each pair fails with probability at most 2 exp(-(k/2)(eps^2/2 - eps^3/3))|Applies the union bound over the n(n - 1)/2 pairs and shows the total is below 1 for the stated k, independent of d"}
:::
