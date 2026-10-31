# Two hundred runs and the compute-optimal frontier

Training compute is about $C = 6ND$ flops (L11). For a fixed budget, choosing $N$ fixes $D = C/(6N)$, and minimizing $L(N, C/6N)$ over $N$ gives the **compute-optimal** model size (Section 6):

$$
N_{\text{opt}}(C) = G\Big(\frac C6\Big)^{\frac\beta{\alpha + \beta}}, \qquad G = \Big(\frac{\alpha A}{\beta B}\Big)^{\frac1{\alpha + \beta}} ,
$$

with $D_{\text{opt}} = C/(6N_{\text{opt}})$. The exponent $\beta/(\alpha + \beta)$ says how to split each extra factor of compute between parameters and data.

- `fit_surface` is provided (e09's solution).
- `optimal_N(chin, C)`: the closed form, from `chin = (E, A, alpha, B, beta)`.
- `optimal_N_numeric(chin, C)`: minimize $L(N, C/6N)$ over $\ln N$ on a fine grid, then refine with a few golden-section steps; return $N$.
- `frontier_exponent(chin)`: $\beta/(\alpha + \beta)$.

The tests fit 200 noisy synthetic runs scattered over three decades of compute, check the frontier exponent within 0.05 of the true $0.45$, and confirm that the numeric optimum matches the closed form.

## Hints

1. Differentiate $AN^{-\alpha} + B(C/6N)^{-\beta}$ in $N$ and set it to zero.
2. The loss is flat near the optimum, so the numeric $N$ agrees with the closed form only to a percent or so unless you refine.
3. The frontier exponent is about one half for Chinchilla's fit: grow parameters and data in roughly equal proportion.
