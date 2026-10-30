import math

import numpy as np

MLP_WIDTHS = [784, 512, 512, 10]
MLP_BATCH = 64
VOCAB, D_MODEL, FLOAT32_BYTES = 50_000, 768, 4
ADAM_PARAMS, ADAM_BYTES_PER_PARAM = 1.3e9, 16
RUN_PARAMS, RUN_TOKENS = 125e6, 2.5e9
GPU_FLOPS, UTILIZATION, PRICE_PER_HOUR = 1e14, 0.4, 2.0
IMAGES, HEIGHT, WIDTH, CHANNELS = 1_281_167, 224, 224, 3
BATCH = 256
SEQ, HEADS, ATT_BATCH = 2048, 12, 8


# provided
def make_corpus(seed=0, n_sentences=3000):
    """3,000 sentences of 8 to 20 words; words of 2 to 9 lowercase letters."""
    rng = np.random.default_rng(seed)
    letters = np.array(list("abcdefghijklmnopqrstuvwxyz"))
    sentences = []
    for _ in range(n_sentences):
        words = ["".join(rng.choice(letters, size=rng.integers(2, 10))) for _ in range(rng.integers(8, 21))]
        sentences.append(" ".join(words) + ".")
    return " ".join(sentences)


CORPUS = make_corpus()

# your answer
ESTIMATES = {
    "mlp_flops": (3e7, 3e8),
    "mlp_params": (3e5, 2e6),
    "embedding_bytes": (5e7, 5e8),
    "adam_gb": (10, 40),
    "train_flops": (1e18, 4e18),
    "gpu_hours": (5, 40),
    "run_cost": (10, 80),
    "imagenet_bytes": (1e11, 4e11),
    "steps_per_epoch": (3000, 8000),
    "attention_entries": (2e8, 8e8),
    "corpus_words": (3e4, 6e4),
    "corpus_chars": (1.5e5, 5e5),
}


def truths():
    """Exact value of each of the twelve quantities, from the constants above."""
    pairs = list(zip(MLP_WIDTHS[:-1], MLP_WIDTHS[1:]))
    flops = 6 * RUN_PARAMS * RUN_TOKENS
    hours = flops / (GPU_FLOPS * UTILIZATION) / 3600
    return {
        "mlp_flops": 2 * MLP_BATCH * sum(a * b for a, b in pairs),
        "mlp_params": sum(a * b + b for a, b in pairs),
        "embedding_bytes": VOCAB * D_MODEL * FLOAT32_BYTES,
        "adam_gb": ADAM_PARAMS * ADAM_BYTES_PER_PARAM / 1e9,
        "train_flops": flops,
        "gpu_hours": hours,
        "run_cost": hours * PRICE_PER_HOUR,
        "imagenet_bytes": IMAGES * HEIGHT * WIDTH * CHANNELS,
        "steps_per_epoch": math.ceil(IMAGES / BATCH),
        "attention_entries": SEQ * SEQ * HEADS * ATT_BATCH,
        "corpus_words": len(CORPUS.split()),
        "corpus_chars": len(CORPUS),
    }


def score(estimates, truths):
    """How many truths lie within a factor of 3 of their interval's geometric midpoint."""
    n = 0
    for name, (lo, hi) in estimates.items():
        mid = math.sqrt(lo * hi)
        t = truths[name]
        if max(mid / t, t / mid) <= 3:
            n += 1
    return n
