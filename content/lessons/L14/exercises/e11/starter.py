def run_collectives(traces):
    """traces[r] is the list of collective ops rank r issues, in order. A collective completes when
    every rank issues it. Return ("ok", count) if all complete; ("mismatch", step, ops) if at some
    step the ranks issue different ops; ("hang", step, waiting) if some ranks have finished while
    the others, listed in waiting, block forever."""
    raise NotImplementedError


def training_trace(losses, consensus):
    """The collectives one rank issues over a run: per step, if consensus, first "all_reduce:flag"
    (all ranks agree whether any loss is nan); then "all_reduce:grads" unless the step is skipped.
    Without consensus a rank skips its gradient all-reduce whenever its own loss is nan; with it,
    every rank skips when any rank's loss is nan. losses[r][t] is rank r's loss at step t.
    Return the list of traces, one per rank."""
    raise NotImplementedError
