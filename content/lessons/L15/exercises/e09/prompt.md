# Paying for inference

A model is trained once and then serves many tokens, each costing about $2N$ FLOPs. If a model will serve $D_\text{inf}$ tokens over its life, the cheapest model to reach a target loss minimizes $6ND + 2ND_\text{inf}$, not $6ND$. `law` is provided.

1. `tokens_needed(N, target, E, A, B, alpha, beta)`: the training tokens a model of $N$ parameters needs to reach `target`, or `np.inf` if even infinite data cannot get it there.
2. `cheapest_model(target, inference_tokens, E, A, B, alpha, beta)`: search 4001 log-spaced sizes from $10^6$ to $10^{13}$ and return $(N, D, \text{total FLOPs})$ of the cheapest.

## Hints

1. Solve $E + A N^{-\alpha} + B D^{-\beta} = \text{target}$ for $D$: $D = \bigl(B / (\text{target} - E - A N^{-\alpha})\bigr)^{1/\beta}$.
2. If $\text{target} - E - A N^{-\alpha} \le 0$ the model is too small.
3. With no inference the answer is the compute-optimal model for the budget that reaches the target; with heavy inference it is smaller and trained on more tokens.
