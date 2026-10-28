# Capstone: clean a crawl, then prove it helped

The notebook builds a noisy crawl from Tiny Shakespeare: the plays cut into about 730 documents, ten copies each of a tenth of them (in different case and spacing), three edited copies of another tenth, a boilerplate footer on most pages, junk pages (keyword spam, number tables, random characters) and forty copies each of a tenth of the validation documents. You write the pipeline: boilerplate removal, exact deduplication, the quality rules, MinHash with LSH, and decontamination. Then the same byte-level GPT trains for the same number of steps on the raw and the cleaned crawl, and both are scored on test text that never leaked and on the leaked and unleaked parts of the validation set.

The autograder checks that every leaked document and nearly all junk is gone, that each source document leaves exactly one survivor, that the cleaned crawl gives a lower test loss at equal compute, and that the raw model's validation score is inflated where the text leaked.

:::exercise{ref=capstone}
:::

:::colab{notebook=L16}
:::

## When you finish

You have built the data side of a training run. L19 feeds a pretraining run through a pipeline like this one and adds the other half: checkpoints, monitoring and recovery.

:::edge{to=L19 text="A pretraining run fed by a resumable pipeline."}
:::
