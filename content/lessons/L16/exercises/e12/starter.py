import numpy as np


def naive_resume(stream, buffer_size, seed, consumed, total):
    """The common bug: on restart, skip the items already read from the stream and start a fresh
    shuffle buffer with the original seed, as if the buffer and the generator had no state."""
    rng = np.random.default_rng(seed)
    out, buffer, pos = [], [], consumed
    while len(out) < total:
        while len(buffer) < buffer_size and pos < len(stream):
            buffer.append(stream[pos])
            pos += 1
        if not buffer:
            break
        out.append(buffer.pop(int(rng.integers(len(buffer)))))
    return out


def shuffle_step(stream, state):
    """One step of a streaming shuffle. state = {"pos", "buffer", "rng", "size"}: fill the buffer
    from stream[pos:] up to size items, then remove and return the item at index
    rng.integers(len(buffer)). Return None when the stream and the buffer are both empty."""
    raise NotImplementedError


def new_state(buffer_size, seed):
    """A fresh shuffle state reading from position 0 with an empty buffer."""
    raise NotImplementedError


def checkpoint(state):
    """Everything needed to resume exactly: position, a copy of the buffer and the generator's
    bit_generator.state."""
    raise NotImplementedError


def restore(saved):
    """A live state from a checkpoint."""
    raise NotImplementedError
