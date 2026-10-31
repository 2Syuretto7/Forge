# Capstone: a cost model of eight algorithms

Eight algorithms are provided with counters: each records how many times it performs its basic operation (an addition, a comparison, a multiply-add), and the matrix multiplications also count how many matrix entries they load from slow memory. Your job is the theory:

1. Derive each count as a sum and write it in closed form.
2. Prove each closed form by induction: give the cost of one more step, so that the tests can check the base case and the step.
3. Predict how each count grows when $n$ doubles, and compare with the counters.

The two matrix multiplications do the same $n^3$ multiply-adds, but the blocked one loads each block once per block product. Counting loads is the first step toward the roofline model of L07, where memory traffic, not arithmetic, decides speed.

:::exercise{ref=capstone}
:::

## When you finish

Sums are how you count, induction is how you prove the counts, and doubling ratios are how you check them against a machine. M06 introduces the logarithm properly (the cost of binary search), M15 makes limits of functions precise, and M29 reads optimizer convergence as a geometric series.

:::edge{to=M08 text="counting arrangements and selections is summing over choices."}
:::
