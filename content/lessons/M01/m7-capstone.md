# Capstone: a Fermi pack of twelve estimates

Twelve quantities from the world of machine learning: dataset sizes, FLOPs, memory and cost. For each one you first write an estimate as an interval, then compute the true value exactly from the data given in the starter, and finally score yourself.

The rule of the capstone is the rule of the lesson: **estimate before you calculate**. Fill in all twelve intervals before you write a line of the `truths` function. Your intervals are the honest record of what you knew; the tests check that at least ten of the twelve true values lie within a factor of 3 of your interval's geometric midpoint, and that each interval is no wider than a factor of 30 from end to end.

:::exercise{ref=capstone}
:::

## When you finish

You can now carry orders of magnitude in your head and check them with code. Every later lesson leans on this:

- M02 names unknowns and solves for them.
- M06 turns "the exponent of ten" into the logarithm, a function you can compute with.
- L11 measures the gap between your browser and a GPU on the roofline.
- M35 fits scaling laws to compute budgets like $6ND$ on log-log axes.

:::edge{to=M06 text="Scientific notation is a logarithm in disguise."}
:::
