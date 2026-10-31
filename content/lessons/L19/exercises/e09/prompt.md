# Activation patching

Which internal component makes a model's output change between two inputs? Run the model on a **corrupted** input, overwrite one component with its value from the **clean** run, and see how much of the output difference comes back.

The provided network decides whether token A appears at position 0 and token B at position 1, through four hidden units. Implement `patch_effects(x_clean, x_corrupt)`: for each hidden unit, the fraction of `output(clean) - output(corrupt)` restored by patching that unit alone.

## Hints

1. Compute both hidden vectors first; patch a copy of the corrupted one.
2. A unit that is the same in both runs has effect 0: patching can only find components that differ.
3. Effects need not sum to 1: components interact, and a fraction above 1 means patching overshoots.
