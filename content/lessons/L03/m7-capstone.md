# Capstone: differentiating real code

Real programs have loops, branches and a mix of functions. Automatic differentiation handles them all, because it differentiates the operations that actually run, not a symbolic formula. Your dual-number library will differentiate a 20-line function exactly, and you will verify it against a careful finite-difference reference.

:::exercise{ref=capstone}
:::

## When you finish

You now own both ends of the differentiation toolbox: finite differences to check, and automatic differentiation to compute. Forward mode was easy to implement because duals carry derivatives along with values. Reverse mode needs a record of the computation, a **tape**, to walk backward. In L08 you will build exactly that: a tensor autograd engine with a tape, whose backward pass uses the VJPs you derived in this lesson.

:::edge{to=L08 text="A reverse-mode engine: record operations on a tape, then run their VJPs backward."}
:::

:::edge{to=L04 text="The softmax VJP meets the derivative of log-probabilities: cross-entropy's gradient."}
:::
