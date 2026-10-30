# Explain it plainly: why rough guesses multiply well

You have derived why estimates work and built tools that use the idea. Now explain it to a curious 12-year-old who knows multiplication but has never heard of a logarithm. If you cannot make it simple, find the step you are hiding behind a formula.

Guidelines:

- Write 150 to 400 words.
- Use one concrete estimate (piano tuners in a city, grains of rice in a bag, the cost of training a model).
- Say why being off "by a factor" is the right way to measure the error.
- Avoid the word logarithm unless you explain it in one plain sentence.

:::feynman{id=f1 prompt="Explain to a 12-year-old why multiplying ten rough guesses together can still give a good answer, and when it does not." key_points="A big unknown number can be built as a product of smaller factors that are each easy to guess roughly|For estimates like this the error is measured as a factor (twice too big, half as big), not as an amount|Multiplying factors means their factor-errors combine, and on a scale of powers of ten that combining is adding|Independent guesses are as likely to be too high as too low, so their errors partly cancel and the total grows only like the square root of the number of guesses|It fails when the guesses are linked, because then all the errors push the same way"}
:::

The grader returns the key points it could not find. Each missing point becomes a review card, and it will come back.
