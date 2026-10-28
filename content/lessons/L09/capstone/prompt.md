# Capstone: an optimizer bake-off

Your optimizers (exercise 8), training loop (exercise 10), a warmup-cosine schedule and the L07 network are provided. Train on `make_digits(2000, 0)`, tune on the validation split `make_digits(1000, 2)`, and report test accuracy on `make_digits(1000, 1)` only for your final recipe.

A recipe is a dictionary with `optimizer` (`"sgd"`, `"momentum"`, `"adam"` for L2 inside Adam, or `"adamw"`), `lr`, `steps` (at most 800), `batch` (at most 100), `schedule` (`"constant"` or `"cosine"`), `warmup`, `weight_decay`, and `momentum` for `"momentum"`.

1. `make_optimizer(recipe)` and `run(recipe, seed=0)`, which trains the L07 network (64-64-32-10) with the recipe and returns the parameters.
2. `BAKEOFF`: for each of the four optimizers, the best recipe you found and its validation accuracy with seed 0, as `{"sgd": {"recipe": {...}, "val_acc": 0.93}, ...}`. The tests rerun every recipe and check your numbers.
3. `RECIPE`: your final choice, which must be at least as good on validation as every bake-off entry (within half a point) and reach at least 92 percent mean test accuracy over seeds 0 and 1.
4. `REPORT`: at least 80 words naming all four optimizers with their validation accuracies, your recipe and its test accuracy, and what made the difference.

Keep the values you report in `BAKEOFF` as numbers you computed; do not tune on the test split.
