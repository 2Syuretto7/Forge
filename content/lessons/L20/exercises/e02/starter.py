import numpy as np


def build_example(prompt, response, bos, sep, eos, pad, max_len):
    """Token ids [bos] + prompt + [sep] + response + [eos], truncated to max_len + 1 and padded with
    pad. Return (inputs, targets, mask), each of length max_len: inputs are the first max_len ids,
    targets the same ids shifted left by one, and mask is 1 exactly where the target is a response
    token or the eos."""
    raise NotImplementedError
