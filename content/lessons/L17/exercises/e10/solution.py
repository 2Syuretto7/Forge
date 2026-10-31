import numpy as np


def softmax(z):
    e = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def rl_arithmetic(steps, lr, group, seed, beta=0.0, theta0=None):
    """A policy answering "a + b mod 10" for digits a, b: logits theta[a, b, :] over the answer
    digit. Each step, for every one of the 100 prompts, sample `group` answers, reward 1 for the
    right digit, compute group advantages (mean-centred, std-normalized with 1e-6), and ascend
    sum (adv * score) / group, minus beta times the gradient of KL(pi || pi0) where pi0 is the
    initial policy. Return (final theta, accuracy of the greedy answers)."""
    rng = np.random.default_rng(seed)
    theta = np.zeros((10, 10, 10)) if theta0 is None else theta0.copy()
    p0 = softmax(theta)
    for _ in range(steps):
        p = softmax(theta)
        g = np.zeros_like(theta)
        for a in range(10):
            for b in range(10):
                acts = rng.choice(10, size=group, p=p[a, b])
                r = (acts == (a + b) % 10).astype(float)
                adv = (r - r.mean()) / (r.std() + 1e-6)
                for act, ad in zip(acts, adv):
                    s = -p[a, b].copy()
                    s[act] += 1
                    g[a, b] += ad * s / group
                if beta:
                    lp = np.log(p[a, b]) - np.log(p0[a, b])
                    kl = np.sum(p[a, b] * lp)
                    g[a, b] -= beta * p[a, b] * (lp - kl)
        theta += lr * g
    greedy = softmax(theta).argmax(axis=2)
    truth = (np.arange(10)[:, None] + np.arange(10)[None, :]) % 10
    return theta, float(np.mean(greedy == truth))
