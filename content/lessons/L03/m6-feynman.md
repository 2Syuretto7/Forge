# Explain it plainly: reverse-mode differentiation

Explain to a programmer who knows only high-school calculus how a computer can get the derivative of a loss with respect to a billion parameters for the cost of a few loss evaluations. Use a small concrete chain of operations as your example.

- Write 150 to 400 words.
- Work through one tiny example with actual numbers.
- Explain why going backward is cheaper than going forward for this problem.
- Say what has to be remembered from the forward pass and why.

:::feynman{id=f1 prompt="Explain how reverse-mode automatic differentiation computes the gradient of a scalar loss with respect to many parameters at the cost of a few loss evaluations, and contrast it with finite differences and forward mode." key_points="A program is a chain of simple operations whose local derivatives are known|The chain rule multiplies local derivatives, and the order of multiplication is a free choice|Going backward from the scalar output computes the derivative with respect to every input in one pass|Going forward or using finite differences needs one pass per input, which is hopeless for a billion parameters|The backward pass needs the intermediate values from the forward pass, which costs memory"}
:::
