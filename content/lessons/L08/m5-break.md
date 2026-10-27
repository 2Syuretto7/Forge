# Break it: in-place updates and broadcasting bugs

## Modifying a tensor the backward pass still needs

Suppose `y = x * w` saved `x` for the gradient of `w`, and before calling `backward()` your code does `x.data *= 2` to "normalize" it. The gradient of `w` is now computed with the doubled `x`: wrong, with no error message. PyTorch prevents this with a version counter on every tensor; the counter increases on each in-place operation, and each backward rule checks that the saved tensors still have the versions they had when they were saved.

:::exercise{ref=e11}
:::

## Broadcasting gradients

The bug from the puzzle, made concrete: an `add` whose backward forgets to unbroadcast hands a $(32, 4)$ gradient to a bias of shape $(4,)$. In NumPy, the update `b -= lr * grad` then either crashes or, worse, broadcasts the update and silently changes the shape of `b`. Your gradient checker from Movement 4 catches it; the next question asks you to predict what it reports.

::::predict{id=p5 kind=choice answer=d}
A bias $b$ of shape $(4,)$ is added to a $(32, 4)$ tensor. The buggy backward returns the first row of the output gradient instead of summing over rows. What does a finite-difference gradient check on $b$ report?

- Agreement: one row is a fair sample.
- A relative error near $10^{-8}$.
- A shape error.
- A large relative error, typically close to 1, because the true gradient is the sum of 32 rows.

:::reveal
The true gradient is the sum over 32 rows; one row is roughly a thirty-second of it (or unrelated to it if rows differ in sign), so the relative error is large, typically above 0.9. Shape checks would not catch this bug, since one row has the correct shape. Only a numerical check does.
:::
::::

## What to take away

- Every operation's backward rule must return gradients with exactly the shapes of its inputs; unbroadcast after every elementwise operation.
- Never modify a tensor in place between the forward and backward passes; if you must, copy it first.
- Check every new operation numerically before using it in a model.
