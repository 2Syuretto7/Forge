# Capstone: a proof portfolio

The starter lists ten true statements in `STATEMENTS`, each with a name and a range of cases to test. For each statement:

1. Write its **predicate** in `PREDICATES`: a function of one case that returns `True` when the statement holds for that case. For the set and logic statements a case is a random instance supplied by the tests (the starter shows the shape of each).
2. Write a **proof** in words in `PROOFS`: at least 40 words, covering every case, not examples.
3. Name the **method** in `METHODS`: one of `"direct"`, `"contrapositive"`, `"contradiction"` or `"cases"`.

Also write `stress(predicate, cases)`, returning the first case where the predicate fails or `None`, so the tests can hunt for counterexamples to your predicates.

The tests check that every predicate survives its stress test, rejects a planted false variant (so your predicates really test something), and that every proof is long enough and names a valid method. The written proofs themselves are graded by you and, below the exercise, by the Feynman grader on the one you choose.
