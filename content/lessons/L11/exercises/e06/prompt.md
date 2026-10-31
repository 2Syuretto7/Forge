# The compute-optimal allocation

`law` is provided.

1. `optimal_allocation(C, E, A, B, alpha, beta)`: the model size $N^*$ and token count $D^* = C/6N^*$ minimizing $L(N, D)$ subject to $6ND = C$, and the loss there, from the closed form you derived.
2. `dloss_dlogN(N, C, E, A, B, alpha, beta)`: the derivative of $L(N, C/6N)$ with respect to $\log N$ at fixed $C$.

## Hints

1. $N^* = G\,(C/6)^{\beta/(\alpha+\beta)}$ with $G = \bigl(\alpha A / (\beta B)\bigr)^{1/(\alpha+\beta)}$.
2. Increasing $\log N$ by $\epsilon$ multiplies $N$ by $e^\epsilon$ and divides $D$ by it, so $\frac{d}{d \log N} = -\alpha A N^{-\alpha} + \beta B D^{-\beta}$.
3. At the optimum the two terms balance: $\alpha A N^{-\alpha} = \beta B D^{-\beta}$.
