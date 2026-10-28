# Recall bridge: tokens, windows and held-out text

From L14: a corpus becomes one long array of token ids, cut into training windows, with validation text split off by position so it is never seen in training. From L06: a test set only measures generalization if nothing about it leaks into training. This lesson scales both ideas to a web crawl, where the same page appears thousands of times, a third of the text is junk, and benchmark questions are copied onto forums. Reviews due from L14 and L06 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
A corpus of 1.2 million characters with 1.88 characters per token holds about [[638298|tol=500]] tokens.
:::
:::step
If a third of it is exact copies of the rest, the unique text is [[0.8|tol=0.001]] million characters.
:::
:::step
If every copied document appears exactly twice, one epoch over the corpus shows each of them to the model [[2]] times, and every other document once.
:::
::::
