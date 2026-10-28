# Tied embeddings

Implement `tied_bigram_loss(E, b, x, y)`: a neural bigram model whose logits are $E[x]\,E^\top + b$, with $E$ of shape $(V, d)$ serving as both the input embedding and the output layer. Return the mean softmax cross-entropy against `y` and the gradients $(\partial L/\partial E, \partial L/\partial b)$.

The gradient of $E$ has two parts: one from its use as the output layer, one from the rows looked up for the inputs.

## Hints

1. With $h = E[x]$ and $G = (\operatorname{softmax} - \text{onehot}(y))/n$: the output part is $G^\top h$.
2. The input part sends $G E$ back to the looked-up rows: `np.add.at(dE, x, G @ E)`, since a token can occur several times.
3. The bias gradient is `G.sum(axis=0)`.
