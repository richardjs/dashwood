'''State representation and operations

States are an array of 4 uint64s, meaning:
    [0] pieces on board
    [1] inverse of pieces on board
    [2] the next piece to be placed
    [3] bitboard of pieces used
    [4] the last space moved (used for quick win calculations)

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

from dashwood import bitboards


def initial():
    s = np.zeros(5, dtype=np.uint64)
    s[3] = 1
    return s


def move(state, space, next_piece):
    '''Apply a move to a state in place. Does not check for validity.'''
    space_offset = space*4
    state[0] = int(state[0]) | (int(state[2]) << space_offset)
    state[1] = int(state[1]) | ((int(~state[2]) & 0b1111) << space_offset)
    state[2] = next_piece
    state[3] = int(state[3]) | (1 << next_piece)
    state[4] = space


def children(state, make_moves=True):
    filled_bits = state[0] | state[1]
    space = 0
    for filled in np.bitwise_and(bitboards.spaces, filled_bits):
        if filled:
            continue

        for piece in range(16):
            piece_bit = 1 << piece
            if int(state[3]) & piece_bit > 0:
                continue

            if make_moves:
                s = state.copy()
                move(s, space, piece)
                yield s
            else:
                yield space, piece

        space += 1


def is_win(s):
    last_space_moved = s[4]
    if (np.bitwise_and(bitboards.wins[last_space_moved], s[0]) == bitboards.wins[last_space_moved]).any():
        return True
    if (np.bitwise_and(bitboards.wins[last_space_moved], s[1]) == bitboards.wins[last_space_moved]).any():
        return True
    return False
