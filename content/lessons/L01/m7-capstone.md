# Capstone: interpreting an embedding set with PCA

This capstone ties the lesson together. You get a cloud of 1,500 embeddings in 48 dimensions and must answer three questions with evidence: how many directions matter, what those directions mean, and what is left over.

The method is the one from Section 8: center, take the SVD, read the explained variance ratios, and inspect the loadings of the top components. The interpretation step is what practitioners do with real embeddings, where the "feature groups" are not labeled and you must infer meaning from which inputs load on a direction.

:::exercise{ref=capstone}
:::

## When you finish

You have now used every major idea in this lesson on one problem. The same pipeline returns several times:

- L06 uses random features and least squares to produce double descent.
- L13 projects token vectors with learned matrices before taking dot products.
- L20 adds a low-rank update to a pretrained weight matrix and trains only its factors.
- L23 searches for interpretable directions in a model's activations, a harder version of the interpretation you just did.

:::edge{to=L13 text="Attention: dot products between learned projections of token vectors."}
:::

:::edge{to=L20 text="LoRA: a trained low-rank update, judged by how much of the full update it captures."}
:::
