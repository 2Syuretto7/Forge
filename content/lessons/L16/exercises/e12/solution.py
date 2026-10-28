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
    while len(state["buffer"]) < state["size"] and state["pos"] < len(stream):
        state["buffer"].append(stream[state["pos"]])
        state["pos"] += 1
    if not state["buffer"]:
        return None
    return state["buffer"].pop(int(state["rng"].integers(len(state["buffer"]))))


def new_state(buffer_size, seed):
    """A fresh shuffle state reading from position 0 with an empty buffer."""
    return {"pos": 0, "buffer": [], "rng": np.random.default_rng(seed), "size": buffer_size}


def checkpoint(state):
    """Everything needed to resume exactly: position, a copy of the buffer and the generator's
    bit_generator.state."""
    return {"pos": state["pos"], "buffer": list(state["buffer"]), "rng": state["rng"].bit_generator.state, "size": state["size"]}


def restore(saved):
    """A live state from a checkpoint."""
    rng = np.random.default_rng()
    rng.bit_generator.state = saved["rng"]
    return {"pos": saved["pos"], "buffer": list(saved["buffer"]), "rng": rng, "size": saved["size"]}
