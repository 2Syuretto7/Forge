# A schedule that survives a restart

Implement `lr_at(step, peak, warmup, total, floor=0.1)`: linear warmup from `peak / warmup` at step 1 to `peak` at step `warmup`, then cosine decay to `floor * peak` at step `total` (and constant after). The rate must depend on nothing but the step, so a resumed run, which only knows its step, continues the same schedule.

## Hints

1. Progress after warmup is $(t - w)/(T - w)$; the cosine factor is $\tfrac12(1 + \cos \pi p)$.
2. Clamp the progress at 1 so a run that continues past `total` stays at the floor.
3. A scheduler object that counts its own calls loses its count on restart unless it too is checkpointed: exercise 12 is that bug.
