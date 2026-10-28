import numpy as np


def static_batching(requests, batch_size):
    """requests: list of (arrival_step, output_tokens), sorted by arrival. A batch starts when the
    server is free and takes up to batch_size waiting requests (waiting until at least one has
    arrived); it runs until its longest request finishes, one token per step. Return each
    request's finish step (in request order)."""
    t, i, finish = 0, 0, [0] * len(requests)
    while i < len(requests):
        t = max(t, requests[i][0])
        batch = [j for j in range(i, len(requests)) if requests[j][0] <= t][:batch_size]
        steps = max(requests[j][1] for j in batch)
        for j in batch:
            finish[j] = t + requests[j][1]
        t += steps
        i = batch[-1] + 1
    return finish


def continuous_batching(requests, batch_size):
    """Iteration-level scheduling: at every step, fill free slots with waiting requests, then every
    running request produces one token; a request leaves as soon as it has all its tokens. Return
    each request's finish step."""
    t, waiting, running, finish = 0, list(range(len(requests))), {}, [0] * len(requests)
    while waiting or running:
        while waiting and len(running) < batch_size and requests[waiting[0]][0] <= t:
            j = waiting.pop(0)
            running[j] = requests[j][1]
        if not running:
            t = requests[waiting[0]][0]
            continue
        t += 1
        for j in list(running):
            running[j] -= 1
            if running[j] == 0:
                finish[j] = t
                del running[j]
    return finish
