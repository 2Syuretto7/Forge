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
    "mlp_flops": None,
    "mlp_params": None,
    "embedding_bytes": None,
    "adam_gb": None,
    "train_flops": None,
    "gpu_hours": None,
    "run_cost": None,
    "imagenet_bytes": None,
    "steps_per_epoch": None,
    "attention_entries": None,
    "corpus_words": None,
    "corpus_chars": None,
}


def truths():
    """Exact value of each of the twelve quantities, from the constants above."""
    raise NotImplementedError


def score(estimates, truths):
    """How many truths lie within a factor of 3 of their interval's geometric midpoint."""
    raise NotImplementedError
