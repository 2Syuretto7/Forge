# Explain it plainly: how autograd works

Explain to a programmer who has used PyTorch but never looked inside how `loss.backward()` computes gradients for code they wrote as an ordinary forward computation.

- Write 150 to 400 words.
- Use a concrete small example such as `loss = ((x * w) + b).sum()`.
- Explain what is recorded during the forward pass, in what order backward runs, and why.
- Mention one way the mechanism can be broken by the user.

:::feynman{id=f1 prompt="Explain how a reverse-mode autograd engine such as PyTorch's computes gradients from an ordinary forward computation, including what is recorded, in which order backward runs, and one way users can break it." key_points="Each operation creates an output that remembers its inputs and a backward rule, building a graph as the code runs|Backward starts from the loss with gradient one and visits nodes in reverse topological order so each gradient is complete before it is passed on|Each backward rule turns the output gradient into input gradients, summing over broadcast dimensions|Gradients from different uses of the same tensor are added, which is why they must be zeroed between steps|Values saved for backward must not be modified in place, and no_grad turns recording off to save memory"}
:::
