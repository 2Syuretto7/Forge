# Capstone: the mathematics of a real paper

Choose one of the three papers of this lesson, DPO, LoRA or Adam, and set `PAPER` to `"dpo"`, `"lora"` or `"adam"`.

1. Implement the reproduction for your paper (the other two may stay unimplemented):
   - `reproduce_dpo()`: train a softmax policy over 8 responses with DPO on 20,000 Bradley-Terry comparisons (reward `np.random.default_rng(0).standard_normal(8)`, uniform reference, $\beta = 0.5$) and return `{"tv": ..., "tv_ref": ...}`, the total variation from the KL-optimal policy of the trained policy and of the reference.
   - `reproduce_lora()`: on e09's task with seed 0, return `{"lora_loss": ..., "full_loss": ..., "fraction": ...}` for rank 4.
   - `reproduce_adam()`: return `{"gd_steps": ..., "adam_steps": ..., "adam_x": ..., "amsgrad_x": ...}` from e13 (curvatures `np.logspace(-2, 2, 50)`, start at ones) and e15.
2. `LESSONS`: the lesson IDs your derivation draws on, at least six, including the ones every derivation of your paper needs (DPO: M27, M30, M36; LoRA: M14, M19, M33; Adam: M16, M24, M29).
3. `EDGES_TRAVELLED`: at least five `(from, to)` pairs, each an edge of the curriculum graph between two of your `LESSONS`, in the direction the graph draws it (horizontal edges count either way).
4. `DERIVATION`: at least 250 words: the paper's central derivation, step by step, naming the lesson each step draws on by its ID.
5. `REPORT`: at least 120 words: what your reproduction measured, which assumption you removed in the break-it exercise and what failed, and how you would explain the paper's idea in five minutes to someone who has finished M15.

The tests check your reproduction against the paper's claim, every lesson and edge against the curriculum graph, and the lengths of the two texts.
