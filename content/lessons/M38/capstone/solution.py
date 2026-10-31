import math
import numpy as np

# your answer
PAPER = "dpo"


def reproduce_dpo():
    """DPO against the KL-optimal policy it should recover."""
    rng = np.random.default_rng(0)
    K, beta, n = 8, 0.5, 20000
    r = rng.standard_normal(K)
    ref = np.log(np.ones(K) / K)
    i = rng.integers(0, K, n)
    j = (i + rng.integers(1, K, n)) % K
    win = rng.random(n) < 1 / (1 + np.exp(-(r[i] - r[j])))
    N = np.zeros((K, K))
    np.add.at(N, (np.where(win, i, j), np.where(win, j, i)), 1)
    z = np.zeros(K)
    for _ in range(3000):
        lp = z - z.max() - np.log(np.sum(np.exp(z - z.max())))
        d = lp - ref
        s = N / (1 + np.exp(beta * (d[:, None] - d[None, :])))
        z += 5.0 * beta * (s.sum(axis=1) - s.sum(axis=0)) / n
    p = np.exp(z - z.max())
    p /= p.sum()
    target = np.exp(ref + r / beta)
    target /= target.sum()
    return {"tv": 0.5 * float(np.abs(p - target).sum()), "tv_ref": 0.5 * float(np.abs(np.exp(ref) - target).sum())}


def reproduce_lora():
    """Rank-4 LoRA against full fine-tuning."""
    rng = np.random.default_rng(0)
    n, k, d = 1500, 32, 24
    X = rng.standard_normal((n, k))
    W0 = rng.standard_normal((k, d)) / np.sqrt(k)
    dW = rng.standard_normal((k, 4)) @ rng.standard_normal((4, d)) / np.sqrt(k) + 0.002 * rng.standard_normal((k, d))
    Y = X @ (W0 + dW) + 0.1 * rng.standard_normal((n, d))
    B = np.zeros((k, 4))
    A = 0.1 * np.random.default_rng(0).standard_normal((4, d))
    C, D = X.T @ X / n, X.T @ Y / n
    for _ in range(1500):
        G = C @ (W0 + B @ A) - D
        B, A = B - 0.1 * G @ A.T, A - 0.1 * B.T @ G
    lora = float(np.sum((X @ (W0 + B @ A) - Y) ** 2) / (2 * n))
    W = np.linalg.lstsq(X, Y, rcond=None)[0]
    full = float(np.sum((X @ W - Y) ** 2) / (2 * n))
    return {"lora_loss": lora, "full_loss": full, "fraction": 4 * (k + d) / (k * d)}


def reproduce_adam():
    """Adam against gradient descent, and Adam against AMSGrad."""
    s = np.logspace(-2, 2, 50)

    def steps(update):
        x = np.ones(50)
        for t in range(1, 50001):
            x = update(x, t)
            if np.all(np.abs(x) < 1e-3):
                return t
        return None

    lr = 1.8 / s.max()
    gd = steps(lambda x, t: x - lr * s * x)
    m, v = np.zeros(50), np.zeros(50)

    def adam(x, t):
        nonlocal m, v
        g = s * x
        m = 0.9 * m + 0.1 * g
        v = 0.999 * v + 0.001 * g * g
        return x - 0.01 * 0.999**t * (m / (1 - 0.9**t)) / (np.sqrt(v / (1 - 0.999**t)) + 1e-12)

    ad = steps(adam)

    def online(amsgrad, C=3.0):
        b2 = 1 / (1 + C * C)
        x, v1, vmax = 0.0, 0.0, 0.0
        for t in range(1, 30001):
            g = C if t % 3 == 1 else -1.0
            v1 = b2 * v1 + (1 - b2) * g * g
            vmax = max(vmax, v1)
            x = min(1.0, max(-1.0, x - 0.5 / math.sqrt(t) * g / (math.sqrt(vmax if amsgrad else v1) + 1e-12)))
        return x

    return {"gd_steps": gd, "adam_steps": ad, "adam_x": online(False), "amsgrad_x": online(True)}


# your answer
LESSONS = ["M22", "M24", "M27", "M29", "M30", "M36", "L17", "M38"]

# your answer
EDGES_TRAVELLED = [("M22", "M27"), ("M27", "M30"), ("M27", "M36"), ("M29", "M36"), ("M24", "M36"), ("M36", "L17"), ("M30", "M38"), ("M36", "M38")]

# your answer
DERIVATION = """
DPO starts from the objective of RLHF: maximize the expected reward of a policy minus beta times
its KL divergence from a reference policy (M27 defines the divergence, M36 explains why the
penalty is needed when the reward is a learned proxy). Maximizing a linear function minus a KL
term over the probability simplex is the constrained problem of M30: its Lagrangian gives the
Gibbs form, pi*(y) = pi_ref(y) exp(r(y) / beta) / Z, where Z normalizes. Taking logarithms and
solving for the reward gives r(y) = beta log(pi*(y) / pi_ref(y)) + beta log Z: the optimal policy
determines the reward up to the constant beta log Z, the same for every response. Preferences
enter through the Bradley-Terry model: the preferred response wins with probability
sigma(r_w - r_l), and fitting rewards to observed comparisons is maximum likelihood, a
cross-entropy (M22 for the expectation, M27 for the loss). Substituting the implied reward,
the constant beta log Z cancels in the difference r_w - r_l, so the likelihood depends only on
the policy: the DPO loss is -log sigma(beta [log pi(y_w)/pi_ref(y_w) - log pi(y_l)/pi_ref(y_l)]).
Its gradient for a softmax policy is beta sigma(-h) times (e_w - e_l), with h the bracketed
margin: a REINFORCE-like update (M36) that raises the winner and lowers the loser, weighted by
how wrong the current policy is about the pair, with no sampling and no reward model. The loss
is minimized by gradient descent (M29). Because the policy is trained on pairs scored by a
Bradley-Terry likelihood, its stationary point is the Gibbs optimum for the reward that
generated the comparisons, which is what the reproduction measures. The derivation needs every
comparison to be uncertain: a deterministic preference makes the margin infinite and the KL
term disappears from the loss (M30 no longer has an interior optimum).
"""

# your answer
REPORT = """
I chose DPO. The reproduction trained a softmax policy over 8 responses on 20,000 simulated
Bradley-Terry comparisons with beta = 0.5 and a uniform reference. The trained policy ended
within 0.032 in total variation of the KL-regularized optimum pi_ref exp(r / beta) / Z that the
derivation predicts, while the reference itself is 0.435 away, so the training moved almost all
the way to the predicted policy without ever seeing a reward. In the break-it exercise I removed
the assumption that preferences are noisy: with one response always winning, the loss kept
falling and the logit gap kept growing after 20,000 steps, because there is no optimum, and the
KL regularization the method was derived from no longer acts. To someone who has finished M15,
I would say: we have a model that picks among answers with probabilities, and people tell us which
of two answers they like better. We nudge the probabilities so that the liked answer becomes more
likely than before relative to a fixed starting model, and less so for the other, by an amount
that shrinks as the model already agrees with the person. Following that slope downhill, like any
derivative, ends at the model people prefer that stays closest to where we started.
"""
