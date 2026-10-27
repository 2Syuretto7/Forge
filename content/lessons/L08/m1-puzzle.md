# Puzzle: how does loss.backward() know what to do?

In PyTorch you write a forward computation as ordinary code, with loops, branches and arbitrary tensor operations, then call `loss.backward()`, and every parameter receives its gradient. You never wrote a backward pass.

::::predict{id=p1 kind=choice answer=b}
How does the framework know which operations to differentiate?

- It parses your Python source code and differentiates it symbolically.
- Every tensor operation, as it runs, records itself and its inputs in a graph; backward walks that graph in reverse.
- It uses finite differences on every parameter.
- It traces the program once and compiles it to a fixed backward program that ignores branches.

:::reveal
PyTorch builds the graph dynamically: each operation creates an output tensor that remembers which function produced it (its `grad_fn`) and which tensors were its inputs. `backward()` sorts that graph and calls each function's backward rule in reverse order. Because the graph is recorded as the code runs, loops and branches just produce whatever graph actually happened.
:::
::::

A second puzzle hides in a single line. You add a bias vector $b$ of shape $(4,)$ to activations $Z$ of shape $(32, 4)$. NumPy and PyTorch **broadcast** $b$ across the 32 rows.

::::predict{id=p2 kind=choice answer=c}
The gradient of the loss with respect to $Z + b$ is a $32 \times 4$ array $G$. What is the gradient with respect to $b$?

- $G$ itself, shape $(32, 4)$.
- The first row of $G$.
- The sum of $G$ over its rows, shape $(4,)$.
- The mean of $G$ over its rows.

:::reveal
$b$ was used 32 times, once per row, so its gradient is the sum of 32 contributions: $G$ summed over the broadcast dimension. Every gradient must have the shape of the tensor it belongs to; whenever the forward pass stretched a tensor, the backward pass sums back over the stretched axes. Getting this wrong (keeping the shape $(32, 4)$, or averaging) is one of the most common autograd bugs.
:::
::::

:::widget{name=ComputationGraph preset=default}
:::

In the widget, $x$ is used twice, by $a = xy$ and by $b = \sin x$. Step through the backward pass and watch its gradient arrive in two pieces that add up. Your engine will do exactly this, for tensors.
