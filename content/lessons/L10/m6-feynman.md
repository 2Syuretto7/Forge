# Explain it plainly: from text to a language model and back

Explain to a programmer how a GPT turns text into numbers for training, what it is trained to do, and how it turns its outputs back into text.

- Write 150 to 400 words.
- Use the example of a short sentence being tokenized.
- Explain byte-pair encoding, the next-token objective, and one sampling control.
- Mention why the loss per token is not enough to compare two models.

:::feynman{id=f1 prompt="Explain how a GPT turns text into tokens for training, what objective it is trained on, and how it generates text, including byte-pair encoding and at least one sampling control." key_points="Byte-pair encoding starts from bytes and merges frequent adjacent pairs into new tokens, so common words become one token and rare text falls back to bytes|The model is trained to predict every next token from the ones before it by minimizing cross-entropy|Generation repeatedly samples a token from the predicted distribution and appends it to the context|Temperature, top-k or top-p reshape the distribution to trade diversity for reliability|Losses per token depend on the tokenizer, so models are compared in bits per character"}
:::
