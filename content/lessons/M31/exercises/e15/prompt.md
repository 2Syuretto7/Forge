# Break it: duplicates in the test set

Hoeffding's inequality needs independent examples. A test set of 1,000 rows that is really 100 distinct examples, each copied 10 times (a common accident of scraped benchmarks), has the variability of 100 examples, not 1,000.

- `duplicated_accuracies(p, unique, copies, sets, rng)`: for `sets` simulated test sets, the measured accuracy when `unique` independent examples (each correct with probability `p`) are each counted `copies` times.
- `naive_coverage(accs, p, rows, delta=0.05)`: the fraction of Hoeffding intervals computed with $n = $ `rows` that contain `p`.
- `effective_n(rows, copies)`: the number of independent examples, `rows / copies`.

The tests find the naive interval covering only about 73 percent of the time at $p = 0.8$, and the interval with the effective $n$ covering more than 99 percent.

## Hints

1. Counting each example 10 times does not change the accuracy, only the claimed precision: simulate the 100 distinct examples and take their mean.
2. Reuse e11's coverage logic.
3. Deduplicate before you evaluate; if you cannot, count the distinct examples.
