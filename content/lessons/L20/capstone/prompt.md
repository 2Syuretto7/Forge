# Capstone: teach a pretrained model two tasks without making it forget

Open the Colab notebook with a **T4 GPU** runtime and work through it:

1. Run the pretraining cell: a byte-level GPT on Tiny Shakespeare, a few minutes on a T4.
2. Write `encode_example`: prompt and answer bytes, with a mask of 0 on the prompt and 1 on the answer (including its final newline).
3. Write `masked_loss`, the mean cross-entropy over the answer positions.
4. Write `LoRALinear.forward` and `LoRALinear.merge`.
5. Fine-tune with LoRA and with every weight, both replaying pretraining text, and compare accuracy on unseen words and the rise in held-out loss.
6. Write a report of at least 80 words: each method's accuracy with intervals, forgetting, trainable parameters, which you would ship, and what replay did.

The autograder checks the encoding, the masked loss, the LoRA layer and its merge, that the adapters are under 15% of the parameters, that LoRA reaches **80%** mean accuracy on unseen words while its held-out loss rises by at most **0.05** nats per byte, and the report.
