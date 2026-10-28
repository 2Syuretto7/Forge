# Capstone: find a circuit and prove it

Open the Colab notebook (a T4 GPU runtime, or the CPU runtime) and work through it:

1. Train the two-layer attention-only model on sequences with a repeated block; the notebook reports its loss on the first and second copies.
2. Write `head_scores`: each head's previous-token score and induction score from its attention pattern. Choose the previous-token heads in layer 0 and the induction heads in layer 1.
3. Write `ablated_loss`: the loss on the second copy with chosen heads mean-ablated. Ablate the previous-token heads, the induction heads, and every other head, and compare.
4. Write `patch_effect`: the fraction of the clean-minus-corrupted metric restored by patching chosen heads' clean outputs into the corrupted run.
5. Write `pair_accuracy` and test the mechanism's prediction on sequences with a single earlier pair, against a control without it.
6. Write a report of at least 80 words: the circuit, the evidence for necessity and sufficiency against the baseline, the prediction, and what the account leaves unexplained.

The autograder checks the scores on a hand-made pattern, that the model learned the task (loss on the second copy below half that on the first), that the circuit has heads in both layers, that ablating either half of it raises the loss on the second copy above 80% of uniform guessing while ablating every other head raises it less than half as much as ablating the circuit, that patching it restores more than 60% of the metric, that the prediction beats the control's interval, and the report.
