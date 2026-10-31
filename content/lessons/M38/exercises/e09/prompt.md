# LoRA at scale: error against rank and parameters

Measure the trade LoRA offers (Section 4): on a task whose true update has rank 4 plus a weak full-rank component, train ranks 1, 2, 4 and 8 and record the loss and the fraction of parameters each trains.

- `rank_sweep(X, Y, W0, ranks, steps=1500)`: a dict from each rank to `(loss, fraction)`, training with e08's method (rewrite it here).
- `full_loss(X, Y)`: the least-squares loss of full fine-tuning.
- `smallest_rank_within(sweep, full, slack=0.05)`: the smallest rank whose loss is within `slack` of the full loss, or `None`.

The tests find rank 4 matching full fine-tuning within 5 percent while training under a third of the parameters, and ranks 1 and 2 clearly worse.

## Hints

1. The fraction is $r(k + d)/(kd)$.
2. Beyond the true rank, extra rank fits only the weak component and the noise: the loss barely moves.
3. In large models $k$ and $d$ are in the thousands and useful ranks are 8 to 64, so the fraction is far below a percent.
