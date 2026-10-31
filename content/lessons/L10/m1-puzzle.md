# Puzzle: what is a token?

Your L09 model read one character at a time: 65 possible symbols, and a context of 128 characters, about two lines of a play. A word-level model would see much further back with the same context length, but its vocabulary would be every word in the language, and any word it never saw in training would be unreadable.

::::predict{id=p1 kind=choice answer=c}
Which tokenization does GPT-style training use?

- Characters, because every string is covered.
- Whole words, with a special token for unknown words.
- Pieces learned from data: frequent sequences of bytes become single tokens, and anything else falls back to individual bytes.
- A fixed list of English syllables.

:::reveal
Byte-pair encoding starts from the 256 possible bytes and learns merges of frequent adjacent pairs: " the" becomes one token, a rare name stays several. Every string is a sequence of UTF-8 bytes, so nothing is ever unknown. The vocabulary size is a dial between characters (small vocabulary, long sequences) and words (huge vocabulary, short sequences).
:::
::::

Step through the merges in the widget, and switch word splitting off to see merges that cross spaces.

:::widget{name=TokenizerStepper}
:::

::::predict{id=p2 kind=choice answer=b}
A model with a BPE vocabulary of 512 reports a validation loss of 2.4 nats per token, and a character-level model reports 1.6 nats per character on the same text. Which is better?

- The character model: 1.6 is less than 2.4.
- You cannot tell until you know how many characters a token covers on average.
- The BPE model, because tokens are better than characters.
- They are equal, because both use cross-entropy.

:::reveal
The losses are per token and per character, different units. If a BPE token covers 1.9 characters on average, 2.4 nats per token is $2.4/1.9 \approx 1.26$ nats per character, better than 1.6. Divide by the characters per token, then by $\ln 2$, to get bits per character, the unit that compares models with different tokenizers.
:::
::::
