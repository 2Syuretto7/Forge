# Reading a profile

A GPU profiler reports, for every kernel, its name, start time and duration. `events` is a list of dictionaries with keys `"name"`, `"start"` and `"dur"` (microseconds) for kernels on one GPU stream, which never overlap.

1. `summarize(events)`: `{name: (count, total_us)}`, ordered from the largest total time to the smallest.
2. `gpu_idle_fraction(events)`: the fraction of the time from the first kernel's start to the last kernel's end during which no kernel runs. A large value means the GPU is waiting for the CPU.
3. `top_fraction(events, k=1)`: the share of all kernel time taken by the `k` names with the largest totals.

## Hints

1. Python dictionaries keep insertion order: build the totals, then `dict(sorted(...))`.
2. Busy time is the sum of durations; the span is from the earliest start to the latest end.
3. `top_fraction` is where optimization should start: the kernels that dominate.
