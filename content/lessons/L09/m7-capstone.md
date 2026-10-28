# Capstone: an optimizer bake-off

Race the optimizers you built on the L07 task, tune each one on a validation split, and write down a recipe that reaches at least 92 percent test accuracy within 800 steps. The L07 baseline, plain SGD at a fixed rate, reached about 90 percent.

:::exercise{ref=capstone}
:::

## When you finish

Your recipe tunes four numbers for one small network. At scale the same questions return with higher stakes: L10 adds normalization so that deep networks stay trainable, L15 asks how the best learning rate moves as models grow, and L19 shows what a learning-rate mistake costs in a long run.

:::edge{to=L10 text="Normalization keeps deep networks trainable after initialization."}
:::
