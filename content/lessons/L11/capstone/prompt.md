# Capstone: predict a run before you train it

Open the Colab notebook with a **T4 GPU** runtime and work through it:

1. Write `non_embedding_params`, the parameter count that scaling laws use.
2. Run the sweep: five model sizes at four token budgets, every run with its own learning-rate schedule.
3. Write `fit_parametric`, the variable-projection fit of $L(N, D) = E + A N^{-\alpha} + B D^{-\beta}$ from exercise 5, over exponents up to 1.5 (the provided `fit_for_exponents` keeps the floor non-negative).
4. Write `optimal_allocation` and compare the fitted frontier with the runs you trained.
5. Record the fit's prediction for the larger held-out model, then train it.
6. Write a report of at least 80 words: the exponents, how close the prediction was, and why the fit could mislead at much larger scale.

The autograder checks the parameter count, the sweep, the frontier, that the fit describes the sweep within **3% relative RMS error**, that the prediction was recorded before the held-out run started and lands within **8%** of it, and the report.
