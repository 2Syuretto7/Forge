# Explain it plainly: cancellation

Explain why subtracting two nearly equal numbers destroys information.

Guidelines:

- Write 150 to 400 words.
- Use a concrete pair of numbers stored to a fixed number of digits.
- Separate the subtraction itself from the errors the inputs already had.
- Give one formula rewritten to avoid the problem.

:::feynman{id=f1 prompt="Explain why subtracting two nearly equal numbers destroys information." key_points="A stored number carries a relative error of about the unit roundoff in its last digits|When two nearly equal numbers are subtracted, their leading digits cancel and only the trailing digits remain|The trailing digits were where the rounding errors lived, so the result's relative error is amplified by the size of the inputs over the size of the difference|The subtraction itself is exact or nearly so; it reveals errors that were already present rather than creating new ones|The fix is to rewrite the formula so the small difference is computed directly, for example 1 - cos x = 2 sin^2(x/2), log1p, expm1, or two-pass variance"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that log sum_i e^{z_i} = m + log sum_i e^{z_i - m} for m = max_i z_i, and that the right side can be evaluated without overflow and without taking the logarithm of zero." key_points="Factors e^m out of the sum: sum e^{z_i} = e^m sum e^{z_i - m}|Takes logarithms, using log(ab) = log a + log b and log e^m = m|Notes that every z_i - m is at most 0, so every exponential is at most 1 and cannot overflow|Notes that the term with z_i = m equals e^0 = 1, so the sum is at least 1 and at most n|Concludes that the logarithm is finite, between 0 and log n, so no infinity or log of zero can occur"}
:::
