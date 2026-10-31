# Capstone: a fast low-rank approximation, placed on the roofline

The starter's `make_matrix(seed=0)` returns a $2000 \times 400$ matrix whose singular values decay geometrically.

1. `rsvd(A, k, p=10, q=1, seed=0)`: `(U, s, Vt)` as in e08.
2. `meets_target(A, U, s, Vt, s_true, k, target=1.01)`: whether the Frobenius error is within `target` times the optimum $(\sum_{j > k}\sigma_j^2)^{1/2}$.
3. `best_time(f, repeats=3)`: the smallest wall-clock time of `repeats` calls of `f()` (`time.perf_counter`).
4. `speedup(A, k=10)`: a dict with `"full"`, the best of two timings of `np.linalg.svd(A, full_matrices=False)`; `"rsvd"`, the best of two timings of your `rsvd(A, k)`; and `"ratio"`, full over randomized.
5. `kernels(m, n, k, p, q)`: one dict per matrix product in the method, in order (the sketch $A\Omega$, then $A^\top Q$ and $AQ$ for each power iteration, then the projection $Q^\top A$), each with `"name"`, `"flops"` ($2 \times$ the three dimensions) and `"bytes"` (fp64, 8 bytes per number, the minimal traffic of e01).
6. `placements(kernel_list, peak, bw)`: each kernel's `"intensity"` and `"bound"`, as in e02, added to its dict.
7. `REPORT`: at least 120 words. Give the error you reached against the optimum, the measured speedup, the intensities of the products and whether each is memory- or compute-bound on the provided laptop-class machine (`PEAK` and `BW` in the starter), and explain why the randomized method is faster even though it does more passes over $A$.

The tests require the error target met at rank 10, a speedup of more than 5, and correct flop and byte counts.
