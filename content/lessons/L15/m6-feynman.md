# Explain it plainly: keeping a long training run healthy

Explain to an engineer joining a pretraining team what can go wrong during a long run and how the team detects and recovers from it.

- Write 150 to 400 words.
- Name at least two causes of loss spikes.
- Explain what a checkpoint must contain for an exact resume, and how a spike is recovered from.
- Mention one bug that makes a resumed run silently different.

:::feynman{id=f1 prompt="Explain what can go wrong during a long pretraining run and how it is detected and recovered from, including causes of loss spikes, what a checkpoint must contain, and one silent resume bug." key_points="Loss spikes come from learning rates that are too high, bad data batches, and numerical problems such as attention or output logits growing without bound|The loss and the gradient norm are logged every step and compared with a trailing window to detect spikes|A checkpoint must contain the model, the optimizer state including its step count, the data position and the random-number states, saved atomically|Recovery restores a checkpoint from before the spike and skips the data around it|A resume that changes the data order or restarts the learning-rate schedule keeps training silently and must be caught by comparing with an uninterrupted run or auditing the logs"}
:::
