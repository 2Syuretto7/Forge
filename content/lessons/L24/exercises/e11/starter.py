def normalize(text):
    return " ".join(text.lower().split())


def leaked_items(eval_prompts, train_prompts):
    """Indices of evaluation prompts that appear, after normalization, among the training prompts."""
    raise NotImplementedError


def honest_accuracy(correct, leaked):
    """Accuracy over all items, over the items that did not leak, and over those that did.
    Return a dict with keys all, clean, leaked (None for an empty group)."""
    raise NotImplementedError
