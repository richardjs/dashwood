'''
State representation

States are an array of 3 uint64s, meaning:
    [0] pieces on board
    [1] inverse of pieces on board
    [2] the next piece to be placed

[1] is not ~[0]. Rather, it is the inverse of the *pieces* on the board.
The inverse calculation is performed when the piece is ORed onto the
bitboard in move(). Note this means piece 0b0000, while
indistinguishable from empty space on [0], is 0b1111 on [1].

Board space numbering:
    0   1   2   3
    4   5   6   7
    8   9   10  11
    12  13  14  15
'''


import numpy as np


def initial():
    return np.zeros(3, dtype=np.int64)


def move(state, space, next_piece, in_place=False):
    if not in_place:
        state = state.copy()

    space_offset = space*4
    state[0] |= state[2] << space_offset
    state[1] |= (~state[2] & 0b1111) << space_offset

    state[2] = next_piece

    return state
