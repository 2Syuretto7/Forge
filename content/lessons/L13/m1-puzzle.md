# Puzzle: which earlier word does "was" need?

Read the sentence "the cat sat on the mat because the cat was tired". To predict what follows "was", a model must know that its subject is "cat", which is six words back, and the distance changes from sentence to sentence. A fixed-size window or a fixed weighting by distance cannot do this; the model needs to **look up** the relevant earlier word by its content.

::::predict{id=p1 kind=choice answer=c}
A lookup over earlier positions needs to be differentiable, so it can be trained by gradient descent. Which mechanism is both content-based and differentiable?

- Pick the single earlier position whose vector is most similar to the current one (an argmax).
- Average all earlier positions equally.
- Score every earlier position by the dot product of a query with its key, softmax the scores, and average the positions' values with those weights.
- Use the position exactly six steps back.

:::reveal
The softmax-weighted average is a soft version of the argmax: when one score dominates, it returns almost exactly that position's value, and it has a gradient everywhere. This is attention. The query says what the current position is looking for, each key says what a position offers, and each value is what it hands over if chosen.
:::
::::

In the widget, choose the previous-token head (every query matches the key of the position before it) and the same-word head, and switch the causal mask on and off.

:::widget{name=AttentionHeatmap pattern=previous d=16}
:::

Now switch back to random projections and increase the head dimension with "Divide logits by sqrt(d)" turned off.

::::predict{id=p2 kind=choice answer=b}
Queries and keys have independent entries of variance 1. Without dividing by $\sqrt d$, what happens to the attention weights as the head dimension grows from 16 to 512?

- Nothing: the softmax normalizes the scores.
- They become nearly one-hot: each row puts almost all its weight on one key.
- They become uniform.
- They become negative.

:::reveal
A dot product of $d$ unit-variance terms has standard deviation $\sqrt d$, so at $d = 512$ the scores differ by tens, and the softmax of such scores is nearly one-hot. A one-hot softmax has almost zero gradient, so the model stops learning which keys to attend to. Dividing by $\sqrt d$ restores unit-scale scores whatever $d$ is.
:::
::::
