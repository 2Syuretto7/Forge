# Rollback and skip

`poisoned_batch(rng, step, bad_steps)` gives a regression batch whose targets are garbage at the steps in `bad_steps`. Implement `run(steps, bad_steps, ...)`: SGD where step $t$'s batch comes from `np.random.default_rng([seed, t])`, a checkpoint every `every` steps, and, when `recover`, a spike check on each step's loss before the update: if it exceeds the mean of the previous `window` kept losses by $k$ standard deviations, restore the checkpoint at `(step - 2) // every * every`, mark every step from there to `skip_ahead` steps past the flagged one as skipped, drop the loss history after the checkpoint, and continue. Return the final weights and the flagged steps.

The run never consults `bad_steps`: like PaLM's recovery, it skips everything seen around the spike.

## Hints

1. Keep the loss history as (step, loss) pairs so you can cut it back to the checkpoint.
2. Generating each step's batch from `(seed, step)` makes skipping trivial: a skipped step's batch is simply never drawn.
3. Compare three runs: clean, poisoned without recovery and poisoned with recovery.
