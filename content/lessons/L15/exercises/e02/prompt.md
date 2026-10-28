# Counting FLOPs

1. `train_flops_per_token(n_params, n_layer, ctx, d)`: six FLOPs per parameter per token (a multiply and an add per weight in forward, twice that in backward), plus attention. In forward, each layer computes the scores $q k^\top$ against all `ctx` keys ($2\,\text{ctx}\,d$ FLOPs per token) and the weighted sum of values (another $2\,\text{ctx}\,d$); backward costs twice the forward. Count masked entries too.
2. `attention_share(ctx, d)`: the fraction of training FLOPs spent on attention when $N = 12\,n_\text{layer}\,d^2$.
3. `tokens_for_budget(C, n_params)`: the tokens a budget of $C$ FLOPs buys, with $C = 6ND$.
4. `mfu(tokens_per_second, flops_per_token, peak_flops)`: model FLOPs utilization, the achieved training FLOP/s as a fraction of the hardware's peak.

## Hints

1. Attention adds $3 \cdot 4\,\text{ctx}\,d = 12\,\text{ctx}\,d$ per layer per token in training.
2. Divide $12\,n_\text{layer}\,\text{ctx}\,d$ by $6 \cdot 12\,n_\text{layer}\,d^2 + 12\,n_\text{layer}\,\text{ctx}\,d$; the layer count cancels.
3. MFU counts the FLOPs the model needs, not the ones the hardware executes, so recomputation (L18) does not raise it.
