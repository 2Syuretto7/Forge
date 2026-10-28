# Explain it plainly: adapting a pretrained model

Explain to an engineer how to adapt a pretrained language model to follow instructions cheaply, and what can go wrong.

- Write 150 to 400 words.
- Explain the fine-tuning loss and why the prompt is masked.
- Explain LoRA and why a low-rank update is usually enough.
- Explain forgetting and how to measure and limit it, and mention distillation.

:::feynman{id=f1 prompt="Explain how supervised fine-tuning and LoRA adapt a pretrained language model to instructions, why a low-rank update is usually enough, and how forgetting is measured and limited; mention distillation." key_points="Supervised fine-tuning maximizes the likelihood of the response given the prompt, with the prompt tokens masked out of the loss|Fine-tuning moves the weights away from the pretrained solution, raising the loss on the original data, which must be measured on a base evaluation|LoRA freezes the weights and learns a low-rank update B A, starting from zero, training far fewer parameters and merging into the weights afterwards|Fine-tuning updates have quickly decaying singular values, so a low rank captures most of the update, as the truncated SVD shows|Distillation trains a small model on a large model's softened output distribution, which carries more information than the correct answer alone"}
:::
