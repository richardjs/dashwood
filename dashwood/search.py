import numpy as np

from dashwood import state
from dashwood.ui.tui import print_state


def minimax(s, depth):
    print('considering:')
    print_state(s)
    if state.is_win(s):
        return -1.0
    if depth == 0:
        return 0.0

    best_v = -np.inf
    for c in state.children(s):
        v = -minimax(c, depth - 1)
        best_v = max(v, best_v)

    return best_v
