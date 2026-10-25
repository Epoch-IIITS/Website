r"""Reference solution for RL-01 Discounted Return.

The recursion G_t = R_{t+1} + γ G_{t+1} lets one backward scan produce every return; G_0 is its first
element.
"""
def returns_to_go(rewards, gamma):
    if not 0 <= gamma <= 1:
        raise ValueError("gamma must be in [0, 1]")
    out = []
    G = 0.0
    for r in reversed(rewards):
        G = r + gamma * G
        out.append(G)
    return out[::-1]


def discounted_return(rewards, gamma):
    rtg = returns_to_go(rewards, gamma)
    return rtg[0] if rtg else 0.0
