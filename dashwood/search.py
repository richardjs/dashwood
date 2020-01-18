from random import choice

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


def montecarlo(s, iterations):
    score = 0
    for _ in range(iterations):
        t = s.copy()
        player_turn = True
        draw = False

        d = 0
        while not state.is_win(t):
            children = list(state.children(t))
            if not children:
                draw = True
                break

            t = choice(list(state.children(t)))
            player_turn = not player_turn

        if not draw:
            if player_turn:
                score += 1
            else:
                score -= 1

    return score/iterations
