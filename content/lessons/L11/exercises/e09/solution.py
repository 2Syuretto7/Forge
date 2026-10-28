def summarize(events):
    """events: dicts with "name", "start" and "dur" (microseconds) for kernels on one GPU stream.
    Return {name: (count, total_us)} sorted by total time, largest first."""
    out = {}
    for e in events:
        c, t = out.get(e["name"], (0, 0.0))
        out[e["name"]] = (c + 1, t + e["dur"])
    return dict(sorted(out.items(), key=lambda kv: -kv[1][1]))


def gpu_idle_fraction(events):
    """Fraction of the span from the first kernel's start to the last kernel's end with no kernel
    running (kernels on one stream do not overlap)."""
    ev = sorted(events, key=lambda e: e["start"])
    start, end = ev[0]["start"], max(e["start"] + e["dur"] for e in ev)
    busy = sum(e["dur"] for e in ev)
    return 1.0 - busy / (end - start)


def top_fraction(events, k=1):
    """Share of all kernel time taken by the k most expensive kernel names."""
    s = summarize(events)
    total = sum(t for _, t in s.values())
    return sum(t for _, t in list(s.values())[:k]) / total
