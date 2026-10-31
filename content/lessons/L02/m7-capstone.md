# Capstone: reproduce double descent and explain the peak

You will reproduce the widget's double-descent curve from scratch on a provided problem, show that its peak is where the design matrix becomes singular, and show that ridge regularization removes it.

:::exercise{ref=capstone}
:::

## When you finish

Large language models live far to the right of every peak in this lesson: billions of parameters, trained on even more tokens, with implicit regularization from the optimizer and explicit regularization from weight decay. L11 studies how their test loss falls with parameters and data, and finds smooth power laws with an irreducible floor, the descendants of this lesson's noise term.

:::edge{to=L11 text="Test loss as a function of model size and data: scaling laws."}
:::
