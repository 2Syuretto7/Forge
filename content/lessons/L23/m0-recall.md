# Recall bridge: the bootstrap, attention heads and trained policies

From L02: an average over a sample is itself a random quantity, and the bootstrap estimates its spread by resampling. From L13: each attention head moves information between positions, chosen by query-key matches. From L21: training with rewards changes a model's behaviour in ways the training reward alone does not reveal. This lesson asks two questions about a trained model: how well does it do, measured honestly, and how does it do it, read from its activations. Reviews due from L02, L13 and L21 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
A model answers 70% of 400 benchmark items correctly. The standard error of its accuracy, $\sqrt{p(1-p)/n}$, is about [[0.0229|tol=0.0002]].
:::
:::step
So a 95% interval runs about $\pm$ [[0.045|tol=0.001]] around 0.70: anything from 65.5% to 74.5% is consistent with the result.
:::
::::
