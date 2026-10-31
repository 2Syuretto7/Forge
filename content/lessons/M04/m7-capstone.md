# Capstone: a ReLU curve builder

Five target curves, each with an error budget, and a budget of 120 ReLU pieces in total. Equally spaced corners would need more than 700 pieces, almost all of them for one curve. You need corners where the curves bend.

Build an adaptive drawer: start with one straight piece, find the piece with the largest error, split it in half, and repeat until every piece is within budget. Then express each drawing as a sum of shifted ReLUs and report how many pieces each curve needed.

:::exercise{ref=capstone}
:::

## When you finish

You have built, by hand, the function class of a one-hidden-layer ReLU network, and placed its corners by an explicit rule. In L03 gradient descent places them for you. Along the way: M05 makes sums of infinitely many pieces precise, M06 inverts the exponential, and M07 composes rotations.

:::edge{to=L03 text="a one-hidden-layer ReLU network is a sum of shifted ReLUs."}
:::
