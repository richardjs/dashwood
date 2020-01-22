'''Bitboards for analysis of states

See state.py for more information about state encoding in bitboards.
'''


def _gen_wins():
    '''Create a series of bitboards for finding winning moves.
    wins[x] gives an array of bitboards to AND against state[0] and
    state[1] to determine if a move just made at space x wins. If any
    AND results in a value > 0, the move was a win.
    '''
    wins = []

    for space in range(16):
        wins.append([])
        for attribute in range(4):
            attribute_bits = 1 << attribute

            winboard = 0
            row_start = (space // 4) * 4
            for i in range(4):
                winboard |= attribute_bits << (4 * (row_start + i))
            wins[space].append(winboard)

            winboard = 0
            col_start = space % 4
            for i in range(4):
                winboard |= attribute_bits << (4 * (col_start + 4*i))
            wins[space].append(winboard)

    return wins


wins = _gen_wins()
