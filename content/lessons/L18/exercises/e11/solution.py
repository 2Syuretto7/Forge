def run_collectives(traces):
    """traces[r] is the list of collective ops rank r issues, in order. A collective completes when
    every rank issues it. Return ("ok", count) if all complete; ("mismatch", step, ops) if at some
    step the ranks issue different ops; ("hang", step, waiting) if some ranks have finished while
    the others, listed in waiting, block forever."""
    step = 0
    while True:
        heads = [t[step] if step < len(t) else None for t in traces]
        if all(h is None for h in heads):
            return ("ok", step)
        if any(h is None for h in heads):
            return ("hang", step, [r for r, h in enumerate(heads) if h is not None])
        if len(set(heads)) > 1:
            return ("mismatch", step, heads)
        step += 1


def training_trace(losses, consensus):
    """The collectives one rank issues over a run: per step, if consensus, first "all_reduce:flag"
    (all ranks agree whether any loss is nan); then "all_reduce:grads" unless the step is skipped.
    Without consensus a rank skips its gradient all-reduce whenever its own loss is nan; with it,
    every rank skips when any rank's loss is nan. losses[r][t] is rank r's loss at step t.
    Return the list of traces, one per rank."""
    ranks, steps = len(losses), len(losses[0])
    traces = [[] for _ in range(ranks)]
    for t in range(steps):
        any_nan = any(l[t] != l[t] for l in losses)
        for r in range(ranks):
            if consensus:
                traces[r].append("all_reduce:flag")
                skip = any_nan
            else:
                skip = losses[r][t] != losses[r][t]
            if not skip:
                traces[r].append("all_reduce:grads")
    return traces
