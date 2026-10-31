MODELS = {
    "1.3B": dict(layers=24, d=2048, heads=16, vocab=50257),
    "13B": dict(layers=40, d=5120, heads=40, vocab=50257),
    "70B": dict(layers=80, d=8192, heads=64, vocab=50257),
}


def params(m):
    return 12 * m["layers"] * m["d"] ** 2 + m["vocab"] * m["d"]


def memory_per_gpu(m, tp, pp, dp, zero, checkpoint, seq=2048, micro=1):
    """Bytes on the most loaded GPU: model states of one tp x pp shard under ZeRO, plus the first
    pipeline stage's activations under 1F1B with FlashAttention."""
    psi = params(m) / (tp * pp)
    states = 2 * psi / (dp if zero >= 3 else 1) + 2 * psi / (dp if zero >= 2 else 1) + 12 * psi / (dp if zero >= 1 else 1)
    layers = -(-m["layers"] // pp)
    per_layer = seq * micro * m["d"] * 34 / tp
    stored = layers * pp * (2 * seq * micro * m["d"] / tp) + per_layer if checkpoint else layers * pp * per_layer
    return states + stored


def find_plan(model, n_gpus, gpu_bytes, node_size=8):
    """The preferred plan that fits in 90% of gpu_bytes. Try tp in (1, 2, 4, 8) up to node_size,
    pp in (1, 2, 4, 8, 16) dividing the layer count, dp = n_gpus / (tp pp) when that is a whole
    number, zero in (0, 1, 2, 3) and checkpoint in (False, True). Prefer, in this order: the
    smallest tp * pp (less model parallelism), then the smallest tp, then the lowest ZeRO stage,
    then no checkpointing. Return a dict with tp, pp, dp, zero, checkpoint and bytes, or None."""
    m = MODELS[model]
    options = []
    for tp in (1, 2, 4, 8):
        for pp in (1, 2, 4, 8, 16):
            if tp > node_size or m["layers"] % pp or n_gpus % (tp * pp):
                continue
            dp = n_gpus // (tp * pp)
            for zero in (0, 1, 2, 3):
                for checkpoint in (False, True):
                    b = memory_per_gpu(m, tp, pp, dp, zero, checkpoint)
                    if b <= 0.9 * gpu_bytes:
                        options.append(((tp * pp, tp, zero, checkpoint), dict(tp=tp, pp=pp, dp=dp, zero=zero, checkpoint=checkpoint, bytes=b)))
    return min(options, key=lambda o: o[0])[1] if options else None
