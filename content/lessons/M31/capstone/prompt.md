# Capstone: an honest evaluation report

The starter's `make_eval(seed=0)` returns the 0/1 correctness vector of a fixed classifier on 2,000 independent test examples.

1. `hoeffding_interval(correct, delta=0.05)` and `bootstrap_interval(correct, B=4000, seed=0, level=0.95)`: `(accuracy, low, high)` as in e07.
2. `union_epsilon(n, k, delta=0.05)`: e04's half-width for $k$ models at once.
3. `reuse_experiment(k=1000, n=1000, seed=0)`: simulate $k$ random-guessing models on one test set of $n$ examples, select the best, evaluate it on a fresh test set of $n$, and return a dict with `"best_test"`, `"fresh"` and `"inflation"` (the difference).
4. `REPORT`: at least 120 words. Give the classifier's accuracy with both intervals and say what each guarantees; give the measured inflation from selecting the best of 1,000 models on one test set; compare it with the union bound's half-width; and say what an evaluator must do differently.

The tests check the intervals, require the inflation between 0.03 and the union bound's $\varepsilon$ for $k = 1000$, $n = 1000$, the fresh accuracy within 0.05 of $0.5$, and a report that mentions Hoeffding, the bootstrap and the union bound.
