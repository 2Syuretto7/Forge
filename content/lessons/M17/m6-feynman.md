# Explain it plainly: speed and distance

Explain why the area under a speed curve is the distance travelled.

Guidelines:

- Write 150 to 400 words.
- Use a car journey with a speed that changes.
- Say what a thin strip of the area means.
- Say how this runs backwards, from distance to speed.

:::feynman{id=f1 prompt="Explain why the area under a speed curve is the distance travelled." key_points="Over a very short time the speed hardly changes, so the distance covered is about speed times time|On a speed-time graph that product is the area of a thin rectangle|Adding the thin rectangles over the whole journey adds up all the little distances|As the time slices shrink, the sum becomes exactly the area under the curve|Conversely, the rate at which the total distance grows is the speed: the fundamental theorem of calculus"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove the fundamental theorem of calculus: if f is continuous on [a, b] and F(x) is the integral of f from a to x, then F'(x) = f(x); deduce that the integral of f from a to b equals G(b) - G(a) for any G with G' = f." key_points="Writes (F(x + h) - F(x)) / h as (1/h) times the integral of f from x to x + h|Bounds that integral between h times the minimum and h times the maximum of f on the strip|By continuity of f both bounds tend to f(x), so F'(x) = f(x)|If G' = f as well, then (G - F)' = 0, so G - F is constant by the mean value theorem|Therefore G(b) - G(a) = F(b) - F(a), which is the integral from a to b"}
:::
