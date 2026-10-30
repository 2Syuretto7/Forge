# Capstone: transform studio

The starter holds a letter F drawn as a polygon and eight target shapes, each the F moved by a linear map, with a description of the moves. For each target, derive the matrix by hand from the description, build it from primitives, and check it numerically against the target and against a matrix fitted to the points by least squares.

:::exercise{ref=capstone}
:::

## When you finish

Every layer of a neural network is a matrix like these followed by a nonlinearity. M11 asks the reverse question, which input produces a given output; M18 finds the matrix that best approximates a curved map near a point; and L13 builds attention from batched products whose shapes you can now read at a glance.

:::edge{to=L13 text="attention is batched matrix products: queries times keys, then weights times values."}
:::
