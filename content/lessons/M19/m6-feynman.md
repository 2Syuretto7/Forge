# Explain it plainly: one backward sweep

Explain how reverse mode can get every partial derivative in one backward sweep.

Guidelines:

- Write 150 to 400 words.
- Use a chain of workers passing a product down a line, or a network of pipes.
- Say what each step needs to know locally.
- Say why going backward, not forward, makes one sweep enough.

:::feynman{id=f1 prompt="Explain how reverse mode can get every partial derivative in one backward sweep." key_points="The forward pass computes and stores every intermediate value of the program|The backward pass starts from the output with sensitivity 1 and moves toward the inputs|Each operation only needs its local derivatives to turn the sensitivity of its result into sensitivities of its arguments|A value used in several places adds up the sensitivities coming back from each use|Because the output is a single number, one backward sweep reaches every input with its partial derivative, whereas going forward would need one sweep per input"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that for Y = X W, with L a scalar function of Y and G = dL/dY, the gradients are dL/dW = X^T G and dL/dX = G W^T." key_points="Perturbs W by a small E so that Y changes by X E|Writes the first-order change of L as the sum over entries of G times the change in Y|Rewrites that sum as the sum over i, j of (X^T G)_ij E_ij, using the definition of the matrix product|Concludes dL/dW = X^T G, and by the same argument with a perturbation of X, dL/dX = G W^T|Checks that the shapes match those of W and X"}
:::
