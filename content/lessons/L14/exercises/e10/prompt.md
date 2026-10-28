# Label smoothing

Implement `smoothed_xent(logits, y, eps)`: the cross-entropy of the model's softmax against the smoothed target $q = (1 - \epsilon)\,\text{onehot}(y) + \epsilon / V$, averaged over the batch, and its gradient with respect to the logits.

Smoothing stops the model from pushing the correct logit to infinity, which can improve calibration; the gradient is still "prediction minus target".

## Hints

1. Loss: $-\tfrac1n \sum_i \sum_j q_{ij} \ln p_{ij}$.
2. Because each row of $q$ sums to 1, the gradient is $(p - q)/n$.
3. With $\epsilon = 0$ you get the ordinary cross-entropy.
