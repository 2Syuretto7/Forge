# Recall bridge: schedules, sizes, data and memory

From L05: the learning rate and its warmup decide whether training is stable at all. From L11: a scaling fit sizes the model and the token budget. From L12: data flows through a pipeline that must resume exactly. From L14: memory and communication shape how the run is laid out. This lesson is about what happens after you press start: a run of days or weeks, on hardware that fails, fed by data that is sometimes broken, and how to keep it on track. Reviews due from L05, L11, L12 and L14 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
Gradient descent on a quadratic with curvature $\lambda = 50$ is stable for learning rates below $2/\lambda =$ [[0.04]].
:::
:::step
A run of 5000 steps that checkpoints every 250 steps writes [[20]] checkpoints.
:::
:::step
If it fails at a random time, it loses on average half an interval: [[125]] steps.
:::
::::
