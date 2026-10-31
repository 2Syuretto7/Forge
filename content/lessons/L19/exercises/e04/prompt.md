# A linear probe

Does a model's hidden state encode a property, such as whether the current token is inside a quotation? Train a linear classifier on the activations and test it on held-out examples.

1. `probe_loss(w, b, A, y, l2=1e-3)`: the mean logistic loss of $\sigma(A w + b)$ plus $\tfrac{l_2}{2}\|w\|^2$, and its gradients.
2. `train_probe(A, y, steps=500, lr=1.0, l2=1e-3)`: gradient descent from zero.
3. `probe_accuracy(w, b, A, y)`.

## Hints

1. With $p = \sigma(z)$ the gradient of the mean loss is $A^\top (p - y)/n$.
2. Keep the probe linear: a probe powerful enough to learn the property itself says nothing about the model.
3. Accuracy on held-out examples is what counts.
