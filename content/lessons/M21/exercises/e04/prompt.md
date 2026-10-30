# Conditional independence

A joint table over three binary variables is a NumPy array `P` of shape `(2, 2, 2)`, indexed `P[a, b, c]`, summing to 1.

- `marginal(P, axes)`: the table over the variables in `axes` (a tuple like `(0, 1)`), summing out the others.
- `independent(P, i, j, tol=1e-12)`: whether variables `i` and `j` are independent in the marginal table over them.
- `cond_independent(P, tol=1e-12)`: whether variables 0 and 1 are independent given variable 2: $P(a, b \mid c) = P(a \mid c)P(b \mid c)$ for every value $c$ with $P(c) > 0$.
- `two_tests(prev, sens, spec)`: the joint table of (test 1, test 2, disease) when both tests have the given sensitivity and specificity and are independent given the disease status.

The tests show the two tests conditionally independent but dependent overall: they agree because they both look at the same disease.

## Hints

1. `P.sum(axis=...)` over the axes not in `axes`.
2. Compare the 2 by 2 table with the outer product of its margins.
3. `P[t1, t2, d] = P(d) P(t1 | d) P(t2 | d)`.
