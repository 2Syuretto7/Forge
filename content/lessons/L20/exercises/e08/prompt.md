# Forgetting

Fine-tuning on a new task moves the weights away from what the pretraining taught. A simple guard pulls them back: add $\tfrac{\lambda}{2}\|w - w_\text{pre}\|^2$ to the fine-tuning loss.

1. `logistic_loss_grad(w, X, y)`: the mean logistic loss and its gradient.
2. `finetune(w_pre, X, y, lam, steps=500, lr=0.5)`: gradient descent from `w_pre` on the new task with the pull.

The tests pretrain on task A, fine-tune on a conflicting task B, and measure the loss on both.

## Hints

1. The pull adds $\lambda (w - w_\text{pre})$ to the gradient.
2. $\lambda = 0$ learns B fully and forgets A; a large $\lambda$ remembers A and barely learns B.
3. The same trade-off is why fine-tuned language models are checked on their base evaluations, not only on the new task.
