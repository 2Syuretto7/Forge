# The SFT loss, masked

Supervised fine-tuning trains on (prompt, response) pairs, but only the response is the model's job: the loss counts response tokens and ignores the prompt.

Implement `masked_ce(logits, targets, mask)`: the mean cross-entropy over the positions where `mask` is 1, and its gradient with respect to the logits, which must be zero at masked-out positions.

## Hints

1. Divide by the number of counted positions, not by the sequence length.
2. The gradient at a counted position is $(\operatorname{softmax}(z) - \text{onehot}(y))/n$.
3. Compute the log-softmax stably by subtracting each row's maximum.
