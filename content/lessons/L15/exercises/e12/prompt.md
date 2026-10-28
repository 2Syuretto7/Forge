# Break it: one learning rate for every size

The best learning rate shrinks as models grow. `sweep_loss(N, lr)` models a sweep in which the best loss for each size follows a power law but is reached only at that size's own best rate; `LRS` and `SIZES` are the sweep.

1. `tuned_losses(sizes, lrs)`: for each size, the lowest loss over `lrs`, and the rate that achieved it.
2. `fixed_lr_losses(sizes, lr)`: each size's loss at one rate.
3. `fitted_exponent(sizes, losses, E)`: the exponent $a$ in $L - E = k N^{-a}$, by a log-log line.

Then compare the exponent of the tuned sweep with that of a sweep that uses the rate tuned for the smallest model everywhere.

## Hints

1. Build a sizes by rates array of losses and take `min` and `argmin` along the rates.
2. Rates too high for the large models make them look worse than they are.
3. A flatter fitted curve means a smaller exponent: you would conclude that scaling up helps less than it does.
