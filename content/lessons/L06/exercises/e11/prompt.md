# Break it: picking the winner by test score

You try `M` "models" that are pure coin flips on a test set of `n_test` examples with random labels, and report the best test accuracy. Then you evaluate that winner on a fresh test set.

- `best_of_m(M, n_test, seed)`: with one `np.random.default_rng(seed)`, draw labels `y` (`n_test` coin flips), then a `(M, n_test)` matrix of random predictions; return `(best_test_accuracy, index_of_best)`.
- `fresh_accuracy(n_fresh, seed)`: the winner's accuracy on fresh data is just another coin-flip experiment; simulate it with a new generator and return the accuracy.
- `expected_max_accuracy(M, n_test)`: an approximation for the best of `M` independent binomial accuracies: $0.5 + \sqrt{2\ln M}\cdot\dfrac{0.5}{\sqrt{n_{\text{test}}}}$.

## Hints

1. Accuracy of row `m`: `np.mean(P[m] == y)`.
2. `np.argmax` over the per-model accuracies.
3. The approximation uses the fact that the maximum of $M$ standard normals is about $\sqrt{2\ln M}$.
