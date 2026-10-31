def normalize(text):
    return " ".join(text.lower().split())


def leaked_items(eval_prompts, train_prompts):
    """Indices of evaluation prompts that appear, after normalization, among the training prompts."""
    seen = {normalize(t) for t in train_prompts}
    return [i for i, p in enumerate(eval_prompts) if normalize(p) in seen]


def honest_accuracy(correct, leaked):
    """Accuracy over all items, over the items that did not leak, and over those that did.
    Return a dict with keys all, clean, leaked (None for an empty group)."""
    leaked = set(leaked)
    def acc(ix):
        return sum(correct[i] for i in ix) / len(ix) if ix else None
    everything = list(range(len(correct)))
    return {"all": acc(everything), "clean": acc([i for i in everything if i not in leaked]),
            "leaked": acc(sorted(leaked))}
