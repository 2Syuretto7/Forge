# The schedule and the step count

The pretraining stage (L19) runs a fixed number of steps chosen from the token budget, with a schedule that depends only on the step.

1. `lr_at(step, peak, warmup, total, floor=0.1)`: linear warmup to `peak` over `warmup` steps, then cosine decay to `floor * peak` at step `total`.
2. `steps_for_tokens(tokens, batch, ctx)`: the steps needed to see `tokens` tokens.

## Hints

1. After warmup, the progress is $(s - w)/(T - w)$, from 0 to 1.
2. The cosine factor $\tfrac12(1 + \cos \pi x)$ goes from 1 to 0.
3. A schedule that is a pure function of the step resumes correctly after a restart.
