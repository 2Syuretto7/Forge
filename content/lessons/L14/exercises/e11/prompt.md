# Break it: collectives that do not match

A collective completes only when every rank calls it. If one rank skips a call, or calls a different one, the others wait forever: the job hangs without an error.

1. `run_collectives(traces)`: `traces[r]` lists rank $r$'s collectives in order. Return `("ok", count)` if all complete, `("mismatch", step, ops)` if the ranks issue different ops at some step, or `("hang", step, waiting)` if some ranks have run out while the ranks in `waiting` block.
2. `training_trace(losses, consensus)`: the traces of a training loop where `losses[r][t]` is rank $r$'s loss at step $t$. Without consensus, a rank skips its gradient all-reduce when its own loss is NaN. With consensus, each step first all-reduces a flag (`"all_reduce:flag"`) so that every rank skips together when any loss is NaN.

## Hints

1. A NaN is the only value not equal to itself: `l != l`.
2. Without consensus, one rank's NaN desynchronizes all later steps.
3. The rule: any decision that changes which collectives run must be the same on every rank, so make it with a collective.
