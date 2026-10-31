# Capstone: a GPT with its own tokenizer

Open the Colab notebook with a **T4 GPU** runtime and work through it:

1. Write `train_bpe` (byte-level, merges within the chunks of the provided pattern, counting each distinct chunk once) and the encoder of one chunk.
2. Write `estimate_loss`: mean validation cross-entropy over windows drawn with a fixed seed, in evaluation mode.
3. Train the provided four-layer GPT with tied embeddings on your tokens; the notebook reports the validation loss in nats per token and in bits per character.
4. Write `filter_logits` for top-k and top-p sampling.
5. Write a report of at least 80 words with your tokenizer's statistics, the validation loss in bits per character, and how samples change with temperature.

The autograder checks that the tokenizer round-trips arbitrary text and compresses, the sampling filters, that training lowers the validation loss, a validation loss below **2.3 bits per character**, and the report.
