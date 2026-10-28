# Train on the response only

Instruction data is a prompt followed by a response, and only the response should be learned (L20). Implement `masked_cross_entropy(logits, targets, mask)`: the mean cross-entropy over positions where `mask` is 1, and its gradient with respect to the logits.

## Hints

1. Subtract each row's maximum before exponentiating.
2. The gradient at a counted position is $(p - \text{onehot}(t))/n$ with $n$ the number of counted positions; elsewhere it is zero.
3. Divide by the number of response tokens, not the sequence length, so short and long responses weigh the same per token.
