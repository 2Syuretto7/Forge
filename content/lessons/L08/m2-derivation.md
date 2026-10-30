# Derivation: the anatomy of an autograd engine

An autograd engine has four ingredients: a tensor that remembers how it was made, a backward rule per operation, a correct order in which to run those rules, and an accounting of what has to be kept in memory. This movement derives each, then maps them onto PyTorch's internals.

## 1. Recording the graph

Each tensor carries its value, a slot for its gradient, references to its parent tensors, and a closure `_backward` that knows how to push its own gradient to its parents. Every operation:

1. computes the output value,
2. creates the output tensor with the inputs as parents,
3. attaches a `_backward` closure that captures whatever the VJP needs (inputs, outputs, shapes).

The result is a directed acyclic graph from the parameters and inputs to the loss.

## 2. The backward rules

You know most of them from M19 and L07. For an output with gradient $G$:

| Operation | Gradient to inputs |
| --- | --- |
| $c = a + b$ | $G$ to $a$, $G$ to $b$ (then unbroadcast) |
| $c = a \odot b$ | $G \odot b$ to $a$, $G \odot a$ to $b$ (then unbroadcast) |
| $C = AB$ | $GB^\top$ to $A$, $A^\top G$ to $B$ |
| $c = \sum a$ (over an axis) | $G$ broadcast back to $a$'s shape |
| $c = e^a$ | $G \odot c$ |
| $c = \log a$ | $G / a$ |
| $c = \max(0, a)$ | $G \odot [a > 0]$ |
| reshape, transpose | apply the inverse reshape or transpose to $G$ |

**Accumulation.** If a tensor is used by several operations, each sends it a contribution, and the chain rule says to add them. So gradients accumulate with `+=`, which is also why training loops must zero gradients before each backward pass.

## 3. Broadcasting and its gradient

NumPy broadcasting aligns shapes from the right; a missing dimension is treated as size 1, and a size-1 dimension is stretched to match. A broadcast input was effectively copied along the stretched axes, so its gradient is the sum of the output gradient over those axes.

::::derivation{id=d1 title="Unbroadcasting a gradient"}
:::step
$a$ has shape $(4,)$ and is added to $Z$ of shape $(32, 4)$. The output gradient has shape $(32, 4)$; summing over axis 0 gives a gradient with [[4]] entries.
:::
:::step
$s$ has shape $(32, 1)$ (one scale per row) and multiplies $Z$ of shape $(32, 4)$. Its gradient is $\sum_j G_{ij} Z_{ij}$ over axis 1, kept as shape $(32, 1)$. If row 0 has $G = (1, 1, 1, 1)$ and $Z = (0.5, -1, 2, 0.5)$, the entry for row 0 is [[2]].
:::
:::step
The general recipe: first sum over the leading axes the input does not have (the output has more dimensions), then sum, keeping dimensions, over every axis where the input had size 1. A scalar added to a tensor of shape $(2, 3, 5)$ receives the sum of all [[30]] entries of the gradient.
:::
::::

## 4. The order of the backward pass

A node may pass its gradient on only when it is complete, which is after every consumer has contributed. Process nodes in **reverse topological order**: build an order in which every node appears after all of its parents (a depth-first search that appends a node after visiting its parents does this), then walk it backwards.

::::derivation{id=d2 title="Ordering a small graph"}
:::step
Graph: $x \to a$, $x \to b$, $(a, b) \to c$, $c \to L$. A valid topological order lists $x$ first and $L$ last. The number of nodes processed before $c$ in the backward pass (starting from $L$) is [[1]].
:::
:::step
In backward, $x$ is processed last. When it is, its gradient already includes the contributions from both $a$ and $b$: [[2]] contributions in total.
:::
:::step
A topological order exists exactly when the graph has no directed cycle. An autograd graph is always acyclic, because each operation creates a new tensor whose parents already existed. The number of possible topological orders of a chain of 5 nodes is [[1]].
:::
::::

## 5. What has to be saved

A backward rule needs some forward values: $\partial(a b)/\partial a$ needs $b$; ReLU needs its input's sign; $\exp$ needs its output; matmul needs both inputs. The engine keeps these alive until backward has used them. That **saved-tensor memory** is usually the largest memory cost of training.

::::derivation{id=d3 title="Counting saved activations"}
:::step
A linear layer $Y = XW + b$ saves $X$ (for $\partial W$) and $W$ (for $\partial X$). With $X$ of shape $(64, 512)$ in float32 (4 bytes), the saved input occupies $64 \cdot 512 \cdot 4 =$ [[131072]] bytes.
:::
:::step
A ReLU after it saves a boolean mask or its input: another $64 \times 512$ values. A network of 24 such blocks with batch 64 and width 512 therefore saves roughly $24 \times 2 \times 64 \times 512 \approx$ [[1572864]] activation values, independent of how many parameters it has.
:::
::::

Inference needs none of this: under `torch.no_grad()` operations record nothing and save nothing. And modifying a saved tensor **in place** after the forward pass would silently change the gradient; frameworks prevent it with a **version counter** on each tensor, checked when the backward rule runs (Movement 5).

:::edge{to=L18 text="Saved activations become the dominant memory term at scale; activation checkpointing trades them for recomputation."}
:::

## 6. The module API

On top of tensors, a small object layer makes models composable: a `Module` owns parameters and submodules, `parameters()` lists them recursively, `zero_grad()` clears their gradients, and `__call__` runs `forward`. An optimizer holds the parameter list and applies an update rule after each backward pass. PyTorch's `nn.Module`, `nn.Linear` and `torch.optim.SGD` are this design, with many more features.

## 7. Mapping onto PyTorch

| Your engine | PyTorch |
| --- | --- |
| `Tensor.data`, `.grad` | `tensor`, `tensor.grad` (leaf tensors with `requires_grad=True`) |
| `_parents`, `_backward` | `tensor.grad_fn` and `grad_fn.next_functions` |
| saved inputs in closures | `ctx.save_for_backward(...)` in an `autograd.Function` |
| topological sort in `backward()` | the autograd engine (C++), running backward nodes in dependency order |
| version check | `RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation` |
| global recording flag | `torch.no_grad()` |

The Colab notebook for this lesson trains the same network with your engine and with PyTorch, walks a real `grad_fn` graph, and writes a custom `torch.autograd.Function`.

:::edge{to=L11 text="Each recorded operation launches at least one GPU kernel; L11 measures the cost of that granularity."}
:::

:::edge{from=M19 text="reverse-mode differentiation and vector-Jacobian products"}
:::

:::edge{from=L07 text="hand-written backward passes for an MLP"}
:::
