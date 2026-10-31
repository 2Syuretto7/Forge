# Derivation: matrices as linear maps

## 1. Linear maps

A function $f$ from $\mathbb{R}^n$ to $\mathbb{R}^m$ is **linear** if it respects addition and scaling:

$$
f(x + y) = f(x) + f(y), \qquad f(c\,x) = c\,f(x) .
$$

Rotations about the origin, reflections, stretches and the projection of M09 are linear. Moving everything one unit to the right is not: it sends $0$ to something nonzero, while a linear map must send $0 = 0 \cdot x$ to $0 \cdot f(x) = 0$.

Write $x = x_1 e_1 + \dots + x_n e_n$, where $e_j$ is the **basis vector** with a 1 in place $j$ and zeros elsewhere. Linearity gives

$$
f(x) = x_1 f(e_1) + \dots + x_n f(e_n) .
$$

So a linear map is decided by the $n$ vectors $f(e_1), \dots, f(e_n)$. Write them side by side as the columns of an $m \times n$ array: that array is the **matrix** $A$ of $f$, and $f(x) = Ax$.

::::derivation{id=d1 title="A matrix is what it does to the basis"}
:::step
A linear map sends $e_1$ to $(2, 1)$ and $e_2$ to $(-1, 1)$. Then $f(3, 2) = 3\,(2, 1) + 2\,(-1, 1)$, whose first coordinate is [[4]].
:::
:::step
Its second coordinate is [[5]].
:::
:::step
The matrix has the images as columns: $A = \begin{pmatrix} 2 & -1 \\ 1 & 1 \end{pmatrix}$. Its entry in row 1, column 2 is [[-1]].
:::
::::

## 2. The matrix-vector product, two ways

The same product reads two ways:

- **By rows**: output $i$ is the dot product of row $i$ of $A$ with $x$: $(Ax)_i = \sum_j A_{ij} x_j$. This is how you compute it.
- **By columns**: $Ax = x_1 (\text{column } 1) + \dots + x_n (\text{column } n)$, a combination of the columns with weights $x$. This is what it means.

The second reading says that the outputs of $A$ are exactly the combinations of its columns, the **column space**, which M11 makes precise. In the widget, $x$ and $y$ are the two columns of $\begin{pmatrix} 2 & -1 \\ 1 & 1 \end{pmatrix}$, and $x + y$ is $A$ times $(1, 1)$.

:::widget{name=VectorPlayground x1=2 x2=1 y1=-1 y2=1 sum=true proj=false}
:::

## 3. Composition is the product

Apply $B$ and then $A$: $x \mapsto A(Bx)$. It is linear, so it has a matrix, written $AB$. Its column $j$ is where $e_j$ ends up: $A$ applied to column $j$ of $B$. Reading that by rows,

$$
(AB)_{ij} = \sum_k A_{ik} B_{kj}
$$

is row $i$ of $A$ dotted with column $j$ of $B$. The shapes must fit: $A$ is $m \times n$, $B$ is $n \times p$, and $AB$ is $m \times p$. The inner sizes match and disappear.

::::derivation{id=d2 title="Rotate and shear, in both orders"}
:::step
$R = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ turns the plane by $90^\circ$ and $H = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ shears it. The entry in row 2, column 2 of $RH$ is row 2 of $R$ dotted with column 2 of $H$: $1 \cdot 1 + 0 \cdot 1 =$ [[1]].
:::
:::step
The same entry of $HR$ is row 2 of $H$ dotted with column 2 of $R$: $0 \cdot (-1) + 1 \cdot 0 =$ [[0]].
:::
:::step
So $RH \neq HR$: shearing then rotating is not rotating then shearing. In $RH$, the map applied **first** is [[word:H/the shear]].
:::
::::

::::predict{id=p3 kind=choice answer=c}
$A$ stretches the plane by 2 along the $x$ axis; $B$ rotates by $90^\circ$. Do $AB$ and $BA$ agree?

- Yes: matrix products always commute.
- Yes, because both are invertible.
- No: rotating first turns the vertical direction onto the horizontal axis, so the stretch lands on a different direction.
- No, but only because $90^\circ$ is a special angle.

:::reveal
No. $AB$ rotates first and then stretches horizontally, which lengthens what started vertical. $BA$ stretches the horizontal first and then rotates it to vertical. Some pairs do commute: two rotations, or anything with a multiple of the identity. Order is the rule, commuting the exception.
:::
::::

Composition of functions is associative, so the product is too: $(AB)C = A(BC)$. The bracketing changes the cost, not the answer, which is how attention implementations choose the cheaper order.

## 4. Identity, inverse, transpose

The **identity** $I$ has ones on the diagonal and zeros elsewhere; $Ix = x$. A square $A$ is **invertible** if some $A^{-1}$ undoes it: $A^{-1}A = AA^{-1} = I$. For 2 by 2,

$$
\begin{pmatrix} a & b \\ c & d \end{pmatrix}^{-1} = \frac{1}{ad - bc} \begin{pmatrix} d & -b \\ -c & a \end{pmatrix} ,
$$

which you can check by multiplying. To undo "do $B$ then $A$", undo $A$ first: $(AB)^{-1} = B^{-1}A^{-1}$, like taking off socks and shoes.

The **transpose** $A^\top$ swaps rows and columns: $(A^\top)_{ij} = A_{ji}$. It moves a matrix across a dot product, $(Ax) \cdot y = x \cdot (A^\top y)$, since both are $\sum_{i,j} A_{ij} x_j y_i$. And $(AB)^\top = B^\top A^\top$: the shapes $(m \times n)(n \times p)$ transpose to $(p \times n)(n \times m)$, which only fit in the reversed order.

::::derivation{id=d3 title="Inverting a 2 by 2 matrix"}
:::step
For $A = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$, $ad - bc =$ [[1]].
:::
:::step
So $A^{-1} = \begin{pmatrix} 1 & -1 \\ -1 & 2 \end{pmatrix}$. Check the top-left entry of $A^{-1}A$: $1 \cdot 2 + (-1) \cdot 1 =$ [[1]].
:::
:::step
When $ad - bc = 0$ the formula divides by zero, and no inverse exists. For $\begin{pmatrix} 1 & 2 \\ 2 & k \end{pmatrix}$ that happens when $k =$ [[4]].
:::
::::

## 5. The determinant: signed area

The unit square goes to the parallelogram spanned by the columns $(a, c)$ and $(b, d)$. Enclose it in the rectangle of sides $a + b$ and $c + d$ (take all entries positive) and subtract what lies outside it: four right triangles, of total area $ac + bd$, and two small rectangles of area $bc$ each:

$$
(a + b)(c + d) - ac - bd - 2bc = ad - bc .
$$

That is the **determinant**, $\det A = ad - bc$. Every small square in the plane is mapped the same way, so every area is multiplied by $|\det A|$. The sign records orientation: negative means a reflection, which turns counterclockwise into clockwise. Since areas scale one map after another, $\det(AB) = \det A \cdot \det B$.

::::derivation{id=d4 title="Areas and determinants"}
:::step
The parallelogram with sides $(3, 1)$ and $(1, 2)$ has area $3 \cdot 2 - 1 \cdot 1 =$ [[5]].
:::
:::step
A rotation keeps areas and orientation, so its determinant is 1; the shear $H$ has determinant 1 as well. Stretching by 2 and 3 along the axes multiplies areas by [[6]].
:::
:::step
$\det A = 0$ means the square is flattened onto a line or a point. Then $A$ has no inverse, because [[word:different points land on the same point/it is not one to one/information is lost]].
:::
::::

For 3 by 3 the determinant is the signed volume of the box spanned by the columns, computed by expanding along the first row:

$$
\det A = a_{11}(a_{22}a_{33} - a_{23}a_{32}) - a_{12}(a_{21}a_{33} - a_{23}a_{31}) + a_{13}(a_{21}a_{32} - a_{22}a_{31}) .
$$

## 6. Blocks and batches

A matrix can be cut into **blocks**, and blocks multiply like entries, as long as the cuts fit: the $(I, J)$ block of $AB$ is $\sum_K A_{IK} B_{KJ}$. GPUs multiply large matrices this way, one tile at a time (L08).

A **batch** is a stack of matrices. NumPy's `A @ B` with shapes $(\beta, m, n)$ and $(\beta, n, p)$ multiplies them pair by pair and returns $(\beta, m, p)$. Each product costs $mp$ dot products of length $n$, that is $2mnp$ floating-point operations (one multiply and one add per term).

::::derivation{id=d5 title="Counting the work in a batched product"}
:::step
One product of two $512 \times 512$ matrices costs $2 \cdot 512^3$ operations. A batch of 64 such products costs [[2*64*512^3]] operations.
:::
:::step
That is about $1.7 \times 10^{10}$. At a sustained $10^{11}$ operations per second it takes about [[0.17|tol=0.01]] seconds.
:::
::::

:::edge{to=M11 text="solving Ax = b runs a matrix backwards; elimination does it and rank says when it cannot."}
:::

:::edge{to=M18 text="the derivative of a function of many variables is a matrix: the best linear map near a point."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Linear map | $f(x + y) = f(x) + f(y)$, $f(cx) = c f(x)$ | layers before their nonlinearity |
| Matrix | columns are the images of $e_1, \dots, e_n$ | build a map from its action |
| $Ax$ | rows dotted with $x$; combination of columns | compute; interpret |
| $AB$ | do $B$, then $A$; shapes $(m \times n)(n \times p)$ | compose maps |
| Inverse | $(AB)^{-1} = B^{-1} A^{-1}$; none when $\det = 0$ | undo a map |
| Transpose | $(Ax) \cdot y = x \cdot A^\top y$; $(AB)^\top = B^\top A^\top$ | gradients (M19) |
| Determinant | area factor, $ad - bc$; $\det AB = \det A \det B$ | invertibility, densities (M20) |
| Batch | $(\beta, m, n)$ @ $(\beta, n, p)$ costs $2\beta mnp$ | attention (L09) |
