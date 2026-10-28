# Recall bridge: the whole path

This lesson adds no new theory. It asks you to use everything at once: clean data (L16), size a model to a budget (L15), pretrain it so the run survives failures (L19), fine-tune it on tasks (L20), improve it with a verifiable reward (L21), measure it honestly (L23) and serve it (L22). The theory half is a design document in which you defend every choice; the practice half runs the pipeline end to end on one T4. Reviews due from all five frontier lessons appear above.

::::derivation{id=d0 title="Warm-up: the budget"}
:::step
A T4 sustains about 2.4 TFLOP/s in float32 on a small model (30% of its 8.1 peak). In ten minutes that is about [[1.44e15|tol=1e13]] floating-point operations.
:::
:::step
At $6N$ operations per token, a model of 10.7 million parameters processes about [[2.24e7|tol=2e5]] tokens with that budget.
:::
::::
