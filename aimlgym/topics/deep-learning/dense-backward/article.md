# Backpropagation Through a Dense Layer

## Learning outcomes

After this lesson you can:

- Derive dX, dW and db for Y = XW + b from the chain rule
- Backpropagate through ReLU
- Compute the mean-squared-error loss and its gradient
- Check every gradient shape against its parameter's shape

## Intuition
DL-10 differentiated one neuron for one example. A dense layer is many neurons
applied to a batch at once: $Y = XW + b$. The same chain rule gives compact matrix formulas, and
there is a simple check: every gradient has exactly the same shape as the thing it is the
gradient of.

## Precise explanation
Shapes: $X$ is $(n, d_{in})$, $W$ is $(d_{in}, d_{out})$, $b$ is $(d_{out},)$, and the upstream
gradient $dY = \partial L/\partial Y$ is $(n, d_{out})$. Then
$$dW = X^\top dY \;(d_{in}, d_{out}), \qquad db = \textstyle\sum_{\text{rows}} dY \;(d_{out},),
  \qquad dX = dY\, W^\top \;(n, d_{in}).$$
Each entry $Y_{ij} = \sum_k X_{ik}W_{kj} + b_j$, so $\partial Y_{ij}/\partial W_{kj} = X_{ik}$; summing
over examples $i$ gives $X^\top dY$. The bias is added to every row, so its gradient sums rows.

**ReLU** $A = \max(0, Z)$: $dZ = dA \cdot [Z > 0]$ (gradient passes where the input was positive).

**MSE loss** over all entries: $L = \frac{1}{m}\sum (\hat Y - Y)^2$ with $m$ the number of
entries, so $\partial L/\partial \hat Y = \frac{2}{m}(\hat Y - Y)$.

**Two-layer network** $H = \mathrm{ReLU}(XW_1 + b_1)$, $\hat Y = HW_2 + b_2$: start from
$d\hat Y$, apply the dense rule for layer 2 (giving $dW_2, db_2, dH$), the ReLU rule, then the
dense rule for layer 1.

## Worked example
$X = [[1, 2]]$, $W = [[1], [-1]]$, $dY = [[3]]$: $dW = X^\top dY = [[3], [6]]$, $db = [3]$,
$dX = dY W^\top = [[3, -3]]$.

## Common mistakes
* $dW = dY^\top X$ — the transpose of the right answer (shape $(d_{out}, d_{in})$).
* Averaging $db$ over the batch when the loss already divided by $n$ (dividing twice).
* ReLU backward using $A > 0$ vs $Z > 0$ is fine, but using `dA > 0` is wrong.

## Why this matters
These four lines are the backward pass of every fully connected network; DL-13
verifies them numerically and DL-19 uses them to train.

## Library implementation

In PyTorch the layer is `torch.nn.Linear(d_in, d_out)` (it stores the weight transposed, shape
`(d_out, d_in)`) and `loss.backward()` computes exactly these gradients. The comparison below
builds the same two-layer network in PyTorch and checks the gradients match; it runs only when
PyTorch is installed.

## References

- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
