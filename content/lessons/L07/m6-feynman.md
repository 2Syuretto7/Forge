# Explain it plainly: backpropagation

Explain backpropagation to someone who understands the chain rule for single-variable functions but has never seen a neural network trained.

- Write 150 to 400 words.
- Use a concrete two-layer example with shapes or numbers.
- Explain what is saved during the forward pass and why.
- Explain why the computation goes backward.

:::feynman{id=f1 prompt="Explain how backpropagation computes the gradient of the loss with respect to every weight of a two-layer neural network, and why it runs backward from the loss." key_points="The network is a chain of layers, each a simple function with a known local derivative|The forward pass computes and saves every layer's inputs and outputs|Starting from the loss, each layer turns the gradient at its output into gradients for its input and its weights using the saved values|A linear layer's weight gradient is its input transposed times the output gradient, and an activation multiplies the gradient by its local slope|Going backward reuses each intermediate gradient for all the weights below it, so the whole gradient costs about two extra forward passes"}
:::
