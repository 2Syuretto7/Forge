# Explain it plainly: doubling digits

Explain why Newton's method doubles the number of correct digits each step.

Guidelines:

- Write 150 to 400 words.
- Use the tangent-line picture.
- Say why the error gets squared, without symbols if you can.
- Say when the doubling stops working.

:::feynman{id=f1 prompt="Explain why Newton's method doubles the number of correct digits each step." key_points="Newton replaces the curve by its tangent line and jumps to where the tangent crosses zero|The gap between the curve and its tangent grows like the square of the distance from the touching point|So the new error is proportional to the square of the old error|Squaring an error of one part in a thousand gives one part in a million: the correct digits double|This holds only near a simple root where the slope is not zero; far away or at a double root the method can fail or slow down"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that if f is twice continuously differentiable, f(r) = 0 and f'(r) is not 0, then the Newton error satisfies e_{k+1} / e_k^2 -> -f''(r) / (2 f'(r)), where e_k = r - x_k." key_points="Expands f(r) around x_k by Taylor's theorem with remainder: 0 = f(x_k) + f'(x_k)(r - x_k) + f''(xi)(r - x_k)^2 / 2|Divides by f'(x_k) and uses x_{k+1} = x_k - f(x_k)/f'(x_k)|Obtains r - x_{k+1} = -f''(xi) / (2 f'(x_k)) times (r - x_k)^2|Uses that xi lies between x_k and r, so xi -> r as x_k -> r, and continuity of f'' and of f' with f'(r) not 0|Concludes the ratio tends to -f''(r) / (2 f'(r)): quadratic convergence"}
:::
