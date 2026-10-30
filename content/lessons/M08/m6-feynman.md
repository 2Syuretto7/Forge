# Explain it plainly: why birthdays collide so early

Explain to a 12-year-old why 23 people are enough for a shared birthday to be more likely than not.

Guidelines:

- Write 150 to 400 words.
- Count pairs rather than people, and say why that is the right thing to count.
- Explain why the answer is not simply 23/365.
- Mention one real use: hash collisions, or lottery numbers, or class photos.

:::feynman{id=f1 prompt="Explain why the birthday collision happens so early, using pairs rather than people." key_points="A match can happen between any two people, so what matters is the number of pairs, not the number of people|23 people make 23 times 22 divided by 2, which is 253 pairs|Each pair matches with chance 1 in 365, so with 253 pairs a match is no longer surprising|It is easiest to compute the chance that nobody matches, by multiplying the chances that each new person avoids everyone before, and subtract it from 1|Pairs grow like the square of the number of people, so collisions start around the square root of the number of possible values"}
:::
