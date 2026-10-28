# Puzzle: teaching a pretrained model a new trick

A pretrained model continues text. You want it to answer instructions instead, using a few thousand examples.

::::predict{id=p1 kind=choice answer=b}
You fine-tune all of the model's weights on the instruction examples. Afterwards, compared with the pretrained model, its loss on ordinary text is:

- Lower, because it has seen more data.
- Higher: fine-tuning moves the weights toward the new task and away from what pretraining taught.
- The same, because the instructions are a small dataset.
- Undefined, because the model now only answers instructions.

:::reveal
Fine-tuning optimizes only the new objective, so nothing holds the weights near the solution pretraining found. The loss on the original distribution rises, sometimes a little, sometimes catastrophically. The capstone measures it, and this lesson's tools (fewer trainable parameters, replaying pretraining data, staying close to the pretrained weights) keep it small.
:::
::::

The widget shows a matrix acting on the plane, with its singular directions. Set the entries close to a rank-one matrix (for example all four near 1): almost all of its action lies along one direction. Fine-tuning updates of large models behave similarly: a few directions carry most of the change.

:::widget{name=MatrixTransform a=1 b=0.9 c=1 d=1.1}
:::

::::predict{id=p2 kind=numeric answer=0.39 tol=0.02}
A LoRA adapter of rank 8 is added to a $4096 \times 4096$ projection. What percentage of that matrix's parameter count does the adapter train?

:::reveal
$8 \cdot (4096 + 4096) = 65{,}536$ parameters against $4096^2 \approx 16.8$ million: about 0.39%. Over a whole model with adapters on only the query and value projections, the fraction of the block parameters is smaller still: about 0.065% for 32 layers of width 4096 (exercise 4).
:::
::::
