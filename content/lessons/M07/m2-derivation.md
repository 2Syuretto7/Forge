# Derivation: triangles, circles, rotations and complex numbers

## 1. Pythagoras

A right triangle has legs $a$, $b$ and hypotenuse $c$. Place four copies inside a square of side $a + b$, each with its right angle at a corner of the square. Their hypotenuses enclose a tilted square of side $c$.

::::derivation{id=d1 title="Pythagoras by rearrangement"}
:::step
The big square's area is $(a + b)^2$. It is also the tilted square plus four triangles: $c^2 + 4 \cdot \frac{ab}{2}$. Expanding $(a + b)^2 = a^2 + 2ab + b^2$ and cancelling $2ab$ gives $c^2 =$ [[a^2 + b^2]].
:::
:::step
So the distance from $(0, 0)$ to $(3, 4)$ is [[5]].
:::
:::step
And the distance between points $(x_1, y_1)$ and $(x_2, y_2)$ is $\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$: for $(1, 2)$ and $(4, 6)$ it is [[5]].
:::
::::

## 2. The unit circle, sine and cosine

The **unit circle** is the set of points at distance 1 from the origin: $x^2 + y^2 = 1$. Start at $(1, 0)$ and walk counterclockwise along it. The angle you have turned determines where you are, and we **define**

$$
\cos \theta = x, \qquad \sin \theta = y
$$

for the point reached after turning by $\theta$. So $\cos^2 \theta + \sin^2 \theta = 1$ always (it is the circle's equation), and sine and cosine are defined for every angle, not just those in a triangle.

**Radians.** Measure an angle by the length of the arc it cuts from the unit circle. A full turn is the whole circumference, $2\pi$; a right angle is $\pi/2$. On a circle of radius $r$, an angle $\theta$ cuts an arc of length $r\theta$. Radians make that formula (and every derivative of sine and cosine, in M15) free of conversion factors, which is why mathematics and every programming library use them.

::::derivation{id=d2 title="Radians and special angles"}
:::step
$180^\circ$ is half a turn, $\pi$ radians, so $30^\circ$ is [[pi/6]] radians.
:::
:::step
In an equilateral triangle of side 1, the height splits the base in half, so $\cos 60^\circ =$ [[1/2]].
:::
:::step
For any angle, $\sin^2 \theta + \cos^2 \theta =$ [[1]].
:::
::::

:::edge{to=M09 text="points of the plane become vectors with lengths and angles, in any number of dimensions."}
:::

## 3. Rotation, and the angle-addition formulas

Rotating the point $(x, y)$ by $\theta$ about the origin is a machine. Where do the two basis points go? $(1, 0)$ goes to $(\cos\theta, \sin\theta)$ by definition, and $(0, 1)$, which starts a quarter turn further on, goes to $(-\sin\theta, \cos\theta)$. Rotation keeps sums and multiples (turning a sum of arrows is turning each and adding), so

$$
R_\theta(x, y) = x(\cos\theta, \sin\theta) + y(-\sin\theta, \cos\theta) = (x\cos\theta - y\sin\theta,\ x\sin\theta + y\cos\theta) .
$$

Turning by $\beta$ and then by $\alpha$ is turning by $\alpha + \beta$. Apply both sides to $(1, 0)$:

::::derivation{id=d3 title="The angle-addition formulas"}
:::step
Turning $(1, 0)$ by $\beta$ gives $(\cos\beta, \sin\beta)$. Turning that by $\alpha$ gives first coordinate $\cos\alpha\cos\beta - \sin\alpha\sin\beta$, which must equal $\cos(\alpha + \beta)$. Writing $a$ for $\alpha$ and $b$ for $\beta$, the second coordinate gives $\sin(a + b) =$ [[sin(a)*cos(b) + cos(a)*sin(b)]].
:::
:::step
With $a = b$: $\cos 2a = \cos^2 a - \sin^2 a$. For $a = 30^\circ$, that is $\frac{3}{4} - \frac{1}{4} =$ [[1/2]], which is $\cos 60^\circ$ as it should be.
:::
::::

Two pages of school trigonometry formulas are this one fact, rotations add, read off in coordinates.

::::predict{id=p3 kind=numeric answer=0.894 tol=0.01}
In Python, `math.sin(90)` returns what? (Python's trigonometric functions take radians.)

:::reveal
About $0.894$, the sine of 90 radians, which is about $5157$ degrees, or $117$ degrees past fourteen full turns. Not 1. Mixing degrees into a radian function produces plausible-looking numbers, which is what makes the bug dangerous; Movement 5 builds a detector for it.
:::
::::

**Polar coordinates.** Any point $(x, y)$ other than the origin is at some distance $r = \sqrt{x^2 + y^2}$ and some angle $\theta$, with $x = r\cos\theta$, $y = r\sin\theta$. The angle is found with the two-argument arctangent, `atan2(y, x)`, which gets the quadrant right.

## 4. Complex numbers

The equation $x^2 = -1$ has no real solution: squares are never negative. As in every extension so far, add a new number $i$ with $i^2 = -1$, and keep all the field rules of M02. Numbers $a + bi$ with real $a$, $b$ are the **complex numbers**. Add them coordinate by coordinate; multiply by expanding and using $i^2 = -1$:

$$
(a + bi)(c + di) = ac + adi + bci + bd\,i^2 = (ac - bd) + (ad + bc)i .
$$

Draw $a + bi$ as the point $(a, b)$. Then multiplying by $i$ sends $x + iy$ to $ix + i^2 y = -y + ix$: the point $(x, y)$ goes to $(-y, x)$. That is a rotation by $90^\circ$.

::::derivation{id=d4 title="Multiplication rotates and scales"}
:::step
Multiplying $3 + 4i$ by $i$ gives $-4 + 3i$. Its real part is [[-4]].
:::
:::step
The **modulus** $|a + bi| = \sqrt{a^2 + b^2}$ is the length of the arrow. For $3 + 4i$ it is [[5]].
:::
:::step
Write $z = r(\cos\alpha + i\sin\alpha)$ and $w = s(\cos\beta + i\sin\beta)$. Multiplying and using the angle-addition formulas, $zw = rs(\cos(\alpha + \beta) + i\sin(\alpha + \beta))$. So the modulus of the product is the product of the moduli, and its angle is the [[word:sum/sum of the angles]] of the angles.
:::
::::

That is the puzzle's number. Multiplying by a complex number of modulus 1 and angle $\theta$ rotates the plane by $\theta$; two such multiplications rotate by the sum of the angles, because multiplication of complex numbers is commutative, and rotations of the plane commute.

## 5. Euler's formula

The number $\cos\theta + i\sin\theta$ behaves like an exponential in $\theta$: multiplying two of them adds their angles, just as $e^a e^b = e^{a+b}$ adds exponents. That suggests **defining**

$$
e^{i\theta} = \cos\theta + i\sin\theta ,
$$

and the definition is consistent with everything in M06: put $x = i\theta$ into the series $e^x = 1 + x + x^2/2! + \dots$, sort the real and imaginary terms, and the two halves are exactly the series for $\cos\theta$ and $\sin\theta$ (you will check it numerically).

::::derivation{id=d5 title="Euler's formula"}
:::step
Half a turn is $\theta = \pi$, where $\cos\pi = -1$ and $\sin\pi = 0$. So $e^{i\pi} =$ [[-1]].
:::
:::step
And $e^{i\alpha} e^{i\beta} = e^{i(\alpha + \beta)}$ says, in coordinates, exactly the angle-addition formulas: the exponential rule for imaginary exponents is the rotation rule. A full turn gives $e^{2\pi i} =$ [[1]].
:::
::::

:::edge{from=M06 text="the exponential of M06, now with an imaginary exponent: it turns instead of grows."}
:::

Every complex number is $z = re^{i\theta}$: a length and an angle. Multiplying multiplies lengths and adds angles. Real exponentials stretch, imaginary ones turn, and a general complex exponential $e^{(a + i\omega)t}$ does both, spiralling: that single fact underlies oscillations, waves, the Fourier transform and, in L09, rotary position embeddings.

:::edge{to=L09 text="rotary position embeddings turn each pair of coordinates of a query and a key by an angle proportional to the token's position, so their dot product depends only on how far apart the tokens are."}
:::

## Summary

| Idea | Statement | Remember |
| --- | --- | --- |
| Pythagoras | $c^2 = a^2 + b^2$ | distance between points |
| Sine and cosine | coordinates on the unit circle | $\sin^2 + \cos^2 = 1$ |
| Radians | arc length on the unit circle | libraries use radians |
| Rotation | $(x\cos\theta - y\sin\theta,\ x\sin\theta + y\cos\theta)$ | rotations add and commute |
| Complex product | $(ac - bd) + (ad + bc)i$ | multiplies lengths, adds angles |
| Euler | $e^{i\theta} = \cos\theta + i\sin\theta$ | $e^{i\pi} = -1$ |
