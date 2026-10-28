import numpy as np


def build_example(prompt, response, bos, sep, eos, pad, max_len):
    """Token ids [bos] + prompt + [sep] + response + [eos], truncated to max_len + 1 and padded with
    pad. Return (inputs, targets, mask), each of length max_len: inputs are the first max_len ids,
    targets the same ids shifted left by one, and mask is 1 exactly where the target is a response
    token or the eos."""
    ids = [bos] + list(prompt) + [sep] + list(response) + [eos]
    first = len(prompt) + 2  # index in ids of the first response token
    kind = [0] * first + [1] * (len(response) + 1)
    ids, kind = ids[: max_len + 1], kind[: max_len + 1]
    ids += [pad] * (max_len + 1 - len(ids))
    kind += [0] * (max_len + 1 - len(kind))
    return np.array(ids[:-1]), np.array(ids[1:]), np.array(kind[1:], dtype=float)
