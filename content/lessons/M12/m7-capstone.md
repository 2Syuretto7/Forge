# Capstone: a curve-fitting service

Six datasets arrive with a basis for each: straight lines, polynomials of growing degree on awkward intervals, and nearly collinear features. Your service fits each by QR least squares, reports diagnostics (residual size, how perpendicular the residual is to the columns, an estimate of the conditioning), and compares itself with a normal-equations baseline. On the ill-conditioned datasets it must be at least a hundred times more accurate.

:::exercise{ref=capstone}
:::

## When you finish

You can fit any linear model and know when to distrust it. M13 takes the projection matrix's eigenvalues, 0 and 1, as the first example of a much larger story, and M14 computes the condition number you have been estimating.

:::edge{to=M13 text="symmetric matrices have orthonormal eigenvectors, and projections are the simplest example."}
:::
