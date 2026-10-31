# Capstone: compressing text

Entropy is a statement about the shortest possible code. In this capstone you build a real code (Huffman's), compress a passage of English with it, and line up the result against three entropy estimates. The comparison makes the lesson concrete: bits per character are the same unit a character-level language model's loss is reported in.

:::exercise{ref=capstone}
:::

## When you finish

A Huffman code assigns each character a fixed codeword based on its frequency alone. Arithmetic coding can use any model's predicted probabilities, character by character, and achieves a length within a couple of bits of the model's total cross-entropy on the text. So a better language model is literally a better compressor, and the cross-entropy you minimize in L10 is the compressed size of the training data in nats.

:::edge{to=L10 text="Your GPT's loss in bits per character is its compression rate on the corpus."}
:::

:::edge{to=L02 text="Held-out cross-entropy as the measure of generalization."}
:::
