# LoRA, break it: an update that is not low-rank

LoRA's assumption is that the update is close to low-rank. Make the true update a random full-rank matrix and the assumption fails: the loss at rank $r$ falls only as fast as the update's singular values allow, and no small $r$ comes close to full fine-tuning (Section 5).

- `train_loss(X, Y, W0, r, steps=1500)`: e08's training, returning the final loss.
- `predicted_floor(X, dW, r, noise_var)`: what the best rank-$r$ update could achieve for this linear model, $\frac1{2n}\big(\lVert X(\Delta W - [\Delta W]_r)\rVert_F^2\big) + \frac d2\sigma^2$ approximately, using the truncated SVD of $\Delta W$ (the inputs here are white, so $X^\top X/n \approx I$).

The tests find rank 4 more than three times worse than full fine-tuning on a full-rank update, and the trained losses tracking the predicted floor within 10 percent.

## Hints

1. With white inputs, $\frac1{2n}\lVert XE\rVert_F^2 \approx \frac12\lVert E\rVert_F^2$ for any error $E$ in the weights.
2. The noise contributes about $\frac d2\sigma^2$ per example whatever the rank.
3. Check the singular values of an update before choosing a LoRA rank, or measure the loss at two ranks and see whether doubling helps.
