import numpy as np

from dashwood import state


def minimax(s, depth):
    if state.is_win(s):
        return -1.0
    if depth == 0:
        return 0.0

    best_v = -np.inf
    for c in state.children(s):
        v = -minimax(c, depth - 1)
        best_v = max(v, best_v)

        if best_v == 1.0:
            break

    return best_v
