import re
import numpy as np


def extract_answer(text):
    """The last integer in the text (with an optional minus sign), or None."""
    found = re.findall(r"-?\d+", text)
    return int(found[-1]) if found else None


def reward(text, answer, want_format=True):
    """1 if the extracted answer equals the true one, else 0; when want_format, a correct answer
    must also appear as "Answer: <n>" (a format check), or it earns 0.5."""
    got = extract_answer(text)
    if got != answer:
        return 0.0
    if want_format and not re.search(r"Answer:\s*-?\d+\s*$", text.strip()):
        return 0.5
    return 1.0


def group_advantages(rewards, eps=1e-6):
    """GRPO-style advantages for a group of samples answering the same prompt: subtract the group
    mean and divide by the group standard deviation (plus eps)."""
    r = np.asarray(rewards, dtype=float)
    return (r - r.mean()) / (r.std() + eps)
