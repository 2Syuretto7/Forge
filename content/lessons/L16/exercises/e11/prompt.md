# Break it: a leaked test set

`make_docs(n, seed)` generates documents from one random word chain, so documents share statistics but not text. Train an $n$-gram language model on training documents, and evaluate it on held-out documents, once clean and once with the evaluation documents leaked into training.

1. `train_counts(docs, n)`: pad each document with $n - 1$ `"<s>"` tokens, and count every context (the previous $n - 1$ words) and every (context, next word). Return the two dictionaries.
2. `avg_logloss(model, docs, n, vocab_size, k=0.1)`: the mean of $-\ln p(w \mid c)$ over every word of `docs`, with $p(w \mid c) = \bigl(\text{count}(c, w) + k\bigr) / \bigl(\text{count}(c) + k V\bigr)$.

## Hints

1. Keys are tuples: the context `tuple(w[i - n + 1:i])` and the $n$-gram `context + (w[i],)`.
2. Add-$k$ smoothing keeps unseen words possible, so the loss stays finite.
3. A model with long contexts memorizes the exact sequences it saw: on leaked documents its loss collapses, which says nothing about new text. The tests also check what this does to model selection: the chain generating the documents is first order, so the bigram model is the right one, yet with the leak a 4-gram model looks far better.
