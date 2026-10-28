import numpy as np


def make_docs(n_docs, seed, length=80, vocab=400):
    """Documents from a random sparse Markov chain over words w0 ... w{vocab-1}: every document
    follows the same chain, so they share statistics but not exact text."""
    rng = np.random.default_rng(1234)
    nxt = rng.integers(0, vocab, (vocab, 6))
    gen = np.random.default_rng(seed)
    docs = []
    for _ in range(n_docs):
        w = int(gen.integers(vocab))
        out = []
        for _ in range(length):
            out.append(f"w{w}")
            w = int(nxt[w, gen.integers(6)]) if gen.random() < 0.9 else int(gen.integers(vocab))
        docs.append(" ".join(out))
    return docs


def train_counts(docs, n):
    """Counts of each context (the n - 1 previous words) and of each (context, next word), with
    documents padded by n - 1 "<s>" tokens. Return (context_counts, ngram_counts) as dicts."""
    ctx, full = {}, {}
    for d in docs:
        w = ["<s>"] * (n - 1) + d.split()
        for i in range(n - 1, len(w)):
            c = tuple(w[i - n + 1:i])
            ctx[c] = ctx.get(c, 0) + 1
            full[c + (w[i],)] = full.get(c + (w[i],), 0) + 1
    return ctx, full


def avg_logloss(model, docs, n, vocab_size, k=0.1):
    """Mean negative log-probability per word under add-k smoothing:
    p(w | c) = (count(c, w) + k) / (count(c) + k vocab_size)."""
    ctx, full = model
    total, count = 0.0, 0
    for d in docs:
        w = ["<s>"] * (n - 1) + d.split()
        for i in range(n - 1, len(w)):
            c = tuple(w[i - n + 1:i])
            p = (full.get(c + (w[i],), 0) + k) / (ctx.get(c, 0) + k * vocab_size)
            total -= np.log(p)
            count += 1
    return total / count
