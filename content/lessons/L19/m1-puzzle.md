# Puzzle: reading a loss curve

The widget replays six real training runs of the same small model, identical until something goes wrong. The first shows a run where steps 700 to 709 trained on corrupted data.

:::widget{name=LossSpikeExplorer run=bad_data compare=healthy}
:::

::::predict{id=p1 kind=choice answer=b}
Select the learning-rate bug: for 60 steps from step 700, the learning rate was 20 times too high, then the schedule continued correctly. By the end of the run, compared with the healthy run, its validation loss is:

- The same: once the rate is back to normal, training recovers.
- Clearly worse, even 400 steps after the bug was over.
- Better, because the higher rate explored more.
- Undefined, because the run diverged.

:::reveal
The logged runs end at 1.64 (healthy) and 2.16 nats (learning-rate bug): sixty bad steps cost more than the whole rest of the run could recover. The corrupted data cost much less (1.65), because each bad step's update was limited by clipping. A spike is not always a blip; restoring a checkpoint from before it is often the only fix.
:::
::::

::::predict{id=p2 kind=choice answer=c}
Switch to the two high-learning-rate runs and the lower panel to the largest attention logit. What does the layer norm on queries and keys change?

- Nothing: the two runs are identical.
- It makes the loss spike more often.
- It keeps the attention logits around 20 instead of hundreds, and the run ends at a lower loss.
- It lowers the learning rate.

:::reveal
Without it, attention logits grow to several hundred, the softmax collapses onto single positions, and training slows (final validation 2.04). With QK-layernorm the logits stay below 20 and the run reaches 1.88. Section 3 of the derivation shows why normalized queries and keys bound the logits.
:::
::::
