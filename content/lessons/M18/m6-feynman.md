# Explain it plainly: gradients and contours

Explain why the gradient is perpendicular to contour lines.

Guidelines:

- Write 150 to 400 words.
- Use a hiking map with contour lines as the picture.
- Say what the gradient is in that picture.
- Say why walking along a contour line costs no height, and what that implies for the steepest direction.

:::feynman{id=f1 prompt="Explain why the gradient is perpendicular to contour lines." key_points="A contour line joins points of equal height, so walking along it the height does not change|The slope in a direction is the gradient dotted with that direction|Along the contour the slope is zero, so the gradient has zero dot product with the contour direction: it is perpendicular to it|The steepest climb goes straight across the contours, along the gradient|Closely spaced contours mean a long gradient, a steep slope"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that for a differentiable f, the directional derivative in a unit direction u is grad f . u, and that it is largest when u points along grad f, with maximum value |grad f|." key_points="Uses the linear approximation f(x + t u) = f(x) + t grad f(x) . u + r(t u) with r(t u) / t -> 0|Divides by t and lets t -> 0 to get the directional derivative grad f . u|Applies Cauchy-Schwarz: |grad f . u| <= |grad f| |u| = |grad f||States that equality holds only when u is a positive multiple of grad f|Concludes the maximum rate is |grad f|, reached along grad f / |grad f| (and the minimum, -|grad f|, along the opposite direction)"}
:::
