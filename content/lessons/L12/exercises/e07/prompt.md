# A quality classifier

Rules catch the obvious junk. GPT-3 and others also trained a linear classifier to tell reference text (books, Wikipedia) from raw web pages, and kept pages that scored like the references. `features(doc)` hashes words and word pairs into a unit-length vector of `DIM` entries.

1. `loss_and_grad(w, b, X, y, l2)`: the mean logistic loss of $\sigma(Xw + b)$ against labels $y \in \{0, 1\}$, plus $\tfrac{l_2}{2}\|w\|^2$, and the gradients with respect to $w$ and $b$ (L01).
2. `train(X, y, steps=300, lr=2.0, l2=1e-3)`: full-batch gradient descent from zero weights; return $(w, b)$.

## Hints

1. `np.logaddexp(0, z) - y * z` is the logistic loss computed without overflow.
2. With $p = \sigma(z)$, the gradient of the mean loss with respect to $z$ is $(p - y)/n$.
3. The classifier learns which words and pairs are typical of the reference text, so it is only as good as the reference set is representative.
